**_Odoo Interlinking Attachments in PDF Report_**

This Odoo module enhances your PDF report generation by allowing interlinking of attachments inside the invoice or other reports. With this functionality, you can seamlessly include clickable links to attached files in your PDF documents, making it easier for users to access additional documents directly from the report.
Key Features

    Interlink Attachments within PDF: Attachments are displayed with clickable links inside the PDF document, enabling direct access to each file.
    File Embedding with Separate Pages: Attachments are not only listed in the invoice footer but are also displayed on their own dedicated pages within the PDF.
    Dynamic PDF Generation: When you generate your PDF report, the system will automatically interlink each attachment to a clickable link.
    Back to Invoice Link: After viewing attachments, users can easily return to the main invoice view with a "Back to Invoice" button, improving navigation.

Installation
Requirements:

    Odoo v14,15.16.17.18 or above
    Python libraries: lxml, PyPDF2 (Install via pip if necessary)
    wkhtmltopdf 0.12.6.1 (with patched qt): This version is required to ensure the correct rendering of PDFs, especially when dealing with complex HTML/CSS or interlinking of attachments in the report.

Installation Steps:

    Install wkhtmltopdf: Ensure you have wkhtmltopdf 0.12.6.1 (with patched qt) installed. If it's not installed or needs to be reinstalled, follow these steps:
        Uninstall the previous version (if applicable):

sudo apt-get remove wkhtmltopdf

Install the required version (0.12.6.1 with patched qt):

        sudo apt-get install wkhtmltopdf

        Alternatively, you can download the appropriate version from the official website.
    Restart your Odoo server after the installation.
    Activate the module via the Odoo Apps interface.
    Once activated, the module will automatically integrate into your existing invoice report.

Usage

Once the module is installed and activated, it will work seamlessly with your existing invoice reports.
How it Works:

    Clickable Links in PDF: Attachments linked to the invoice are added as clickable items in the PDF. Users can click these links to download the attached files directly from the report.
    Interlinking Attachments: Attachments are listed in a special section, with each file having its own link. This allows recipients of the invoice to easily access the attachments without leaving the document.
    Separate Attachment Pages: Each attachment is also shown on its own page in the PDF report, making them viewable in full detail.

Example of Interlinked Attachment in the Invoice PDF:

<xpath expr="//td[@class='text-end o_price_total'][last()]" position="after">
    <td>
        <t t-foreach="line.attachment_ids" t-as="attachment">
            <li>
                <a t-att-href="'#attachment_%s' % attachment.id"
                   style="color: blue; text-decoration: underline;">
                    <span t-field="attachment.name"/>
                </a>
            </li>
        </t>
    </td>
</xpath>

Attachments Display:

    Attachments will appear in the footer section of the invoice under a new "Attachment" column. Each attachment is clickable, making it easy for users to open or download.
    Additionally, each attachment will be displayed on its own page in the PDF report, ensuring they are neatly presented and accessible.

Back to Invoice Link:

    At the bottom of each attachment page, there is a clickable "Back to Invoice" link that takes users back to the main invoice, improving navigation within the document.

Customization

The module's template can be customized to adjust the display or add extra styling to how the attachments appear within the PDF.

For example, you can modify the template to customize the link appearance or change the positioning of the attachment list.

To customize, modify the report_invoice_document template in your Odoo instance as needed.

<xpath expr="//table[@class='table table-sm o_main_table table-borderless']/thead/tr/th[@name='th_subtotal']" position="after">
    <th name="th_attachment" class="text-start"><span>Attachment</span></th>
</xpath>

Troubleshooting
Issue 1: Attachments Not Showing

    If attachments do not show up in the generated PDF, check that the invoice has attachments. The attachment section will only display if the invoice contains files.

Issue 2: "Back to Invoice" Link Missing

    Ensure the attachments are properly rendered. If there are no attachments, the "Back to Invoice" link might not appear.

Issue 3: Formatting Issues

    If the layout doesn’t look as expected, you may need to tweak the HTML and CSS in the report template to match your company’s design needs.

Contributing

If you have suggestions for improvements, bug fixes, or new features, feel free to contribute by forking the repository and submitting a pull request. We welcome contributions from the community!
License

This module is licensed under the Odoo Proprietary License. Please refer to the official Odoo documentation for licensing terms.

This version highlights the importance of installing the wkhtmltopdf 0.12.6.1 (with patched qt) version and includes steps on how to uninstall and reinstall it. Let me know if this works for you!