from odoo import fields, models


class AccountMoveLine(models.Model):
    """Account move line """
    _inherit = 'account.move.line'

    book_id = fields.Many2one(comodel_name='library.book')