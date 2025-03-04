from odoo import api, fields, models
from odoo import models, fields, api
import PyPDF2
import base64
from io import BytesIO

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    attachment_ids = fields.One2many(
        'ir.attachment', 'res_id', string="Attachments",
        domain=[('res_model', '=', 'account.move.line')]
    )


class AccountMove(models.Model):
    _inherit = 'account.move'













