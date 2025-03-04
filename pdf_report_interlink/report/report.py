from odoo import models, fields, api
from io import BytesIO
from PyPDF2 import PdfMerger
import base64
import logging

_logger = logging.getLogger(__name__)

class ReportInvoiceWithoutPayment(models.AbstractModel):
    _name = 'report.account.report_invoice'
    _description = 'Account report without payment lines'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['account.move'].browse(docids)
        qr_code_urls = {}

        for invoice in docs:
            if invoice.display_qr_code:
                new_code_url = invoice._generate_qr_code(silent_errors=data['report_type'] == 'html')
                if new_code_url:
                    qr_code_urls[invoice.id] = new_code_url

        # Return the standard report values along with qr_code_urls
        return {
            'doc_ids': docids,
            'doc_model': 'account.move',
            'docs': docs,
            'qr_code_urls': qr_code_urls,
        }


class ReportInvoiceWithPayment(models.AbstractModel):
    _name = 'report.account.report_invoice_with_payments'
    _description = 'Account report with payment lines'
    _inherit = 'report.account.report_invoice'

    @api.model
    def _get_report_values(self, docids, data=None):
        rslt = super()._get_report_values(docids, data)
        invoices = self.env['account.move'].browse(docids)
        base_pdf = self._generate_invoice_pdf(invoices)
        merged_pdf = self._merge_pdf_with_attachments(invoices, base_pdf)

        rslt['merged_pdf'] = base64.b64encode(merged_pdf).decode('utf-8')
        rslt['report_type'] = data.get('report_type') if data else ''

        return rslt

    def _generate_invoice_pdf(self, invoices):
        report_ref = 'account.report_invoice'

        try:
            if isinstance(report_ref, list):
                raise ValueError(f"Expected a string for report_ref, but got a list: {report_ref}")
            if not report_ref:
                raise ValueError("The report_ref cannot be empty or None.")
            report_action = self.env['ir.actions.report']._get_report_from_name(report_ref)

            pdf_report, _ = report_action.sudo()._render_qweb_pdf(invoices.ids)
            return BytesIO(pdf_report)
        except Exception as e:
            _logger.error(f"Error generating PDF for invoices {invoices.ids}: {e}")
            raise ValueError(f"Error generating PDF for invoices {invoices.ids}: {e}")

    def _merge_pdf_with_attachments(self, invoices, base_pdf):
        try:
            merger = PdfMerger()
            merger.append(base_pdf)

            for invoice in invoices:
                for line in invoice.invoice_line_ids:
                    for attachment in line.attachment_ids:
                        if attachment.mimetype == 'application/pdf' and attachment.datas:
                            try:
                                attachment_data = base64.b64decode(attachment.datas)
                                attachment_pdf = BytesIO(attachment_data)
                                merger.append(attachment_pdf)
                            except Exception as e:
                                _logger.error(f"Error merging attachment for invoice {invoice.id}: {e}")
                                continue

            merged_pdf_stream = BytesIO()
            merger.write(merged_pdf_stream)
            merged_pdf_stream.seek(0)

            return merged_pdf_stream.read()
        except Exception as e:
            _logger.error(f"Error merging PDFs: {e}")
            raise ValueError(f"Error merging PDFs: {e}")
