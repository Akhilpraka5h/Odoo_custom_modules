from odoo import fields, models


class Recommendation(models.Model):
    """Create recommendation for checkouts"""
    _name = 'recommendation'
    _description = 'Recommendations'

    book_title = fields.Char(string='Name', required=True)
    book_cover_image = fields.Image(string='Cover Image')
    select_book = fields.Boolean(string='Select', default=False)
    checkout_id = fields.Many2one(comodel_name='book.checkout')
    recommendation_id = fields.Many2one(comodel_name='recommended.book',
                                        string='Recommendation ')
