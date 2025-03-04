from markupsafe import Markup
from odoo import api, fields, models, tools, SUPERUSER_ID, _
import logging
import os
import lxml.html

from lxml import etree
from PIL import Image, ImageFile
# Allow truncated images
ImageFile.LOAD_TRUNCATED_IMAGES = True
wkhtmltopdf_dpi_zoom_ratio = False

try:
    from PyPDF2.errors import PdfReadError
except ImportError:
    from PyPDF2.utils import PdfReadError

_logger = logging.getLogger(__name__)
_DEFAULT_BARCODE_FONT = 'Courier'

class IrActionsReport(models.Model):
    _inherit = 'ir.actions.actions'

    def _prepare_html(self, html, report_model=False):
        layout = self._get_layout()
        if not layout:
            return {}
        base_url = ""
        # Parse HTML using lxml
        root = lxml.html.fromstring(html, parser=lxml.html.HTMLParser(encoding='utf-8'))
        match_klass = "//div[contains(concat(' ', normalize-space(@class), ' '), ' {} ')]"

        header_node = etree.Element('div', id='minimal_layout_report_headers')
        footer_node = etree.Element('div', id='minimal_layout_report_footers')
        bodies = []
        res_ids = []

        body_parent = root.xpath('//main')[0] if root.xpath('//main') else root

        # 🔹 Fixed internal links
        for a in root.xpath('//a[starts-with(@href, "#")]'):
            href_value = a.get("href")
            if href_value:
                a.set("href", href_value)
                a.set("target", "")
                a.set("rel", "noopener noreferrer nofollow")
            else:
                a.drop_tag()

        for annotation in root.xpath('//section[contains(@class, "linkAnnotation")]'):
            annotation.drop_tree()

        for anchor in root.xpath('//a[@id]'):
            anchor.set("style", "display:block; height:1px; visibility:hidden;")

        for node in root.xpath(match_klass.format('header')):
            body_parent = node.getparent()
            node.getparent().remove(node)
            header_node.append(node)

        for node in root.xpath(match_klass.format('footer')):
            body_parent = node.getparent()
            node.getparent().remove(node)
            footer_node.append(node)

        for node in root.xpath(match_klass.format('article')):
            IrQweb = self.env['ir.qweb']
            if node.get('data-oe-lang'):
                IrQweb = IrQweb.with_context(lang=node.get('data-oe-lang'))
            body = IrQweb._render(layout.id, {
                'subst': False,
                'body': Markup(lxml.html.tostring(node, encoding='unicode')),
                'base_url': base_url,
                'report_xml_id': self.xml_id
            }, raise_if_not_found=False)
            bodies.append(body)
            res_ids.append(int(node.get('data-oe-id', 0)) if node.get('data-oe-model') == report_model else None)

        if not bodies:
            body = ''.join(lxml.html.tostring(c, encoding='unicode') for c in body_parent.getchildren())
            bodies.append(body)

        specific_paperformat_args = {attr[0]: attr[1] for attr in root.items() if attr[0].startswith('data-report-')}

        header = self.env['ir.qweb']._render(layout.id, {
            'subst': True,
            'body': Markup(lxml.html.tostring(header_node, encoding='unicode')),
            'base_url': base_url
        })
        footer = self.env['ir.qweb']._render(layout.id, {
            'subst': True,
            'body': Markup(lxml.html.tostring(footer_node, encoding='unicode')),
            'base_url': base_url
        })

        return bodies, res_ids, header, footer, specific_paperformat_args

        # Base Method Debugged and checked  for the common arguments  ------[command_args]    Not Required  def _build_wkhtmltopdf_args
        return super(IrActionsReport, self)._prepare_html()

