from odoo import fields,models


class RecentViewProduct(models.Model):
    """Recent View products"""
    _name = 'recent.view.product'
    _description = 'Recently viewed product'


    partner_id = fields.Many2one(comodel_name='res.partner')
    product_template_id = fields.Many2one(comodel_name='product.template')
    view_date = fields.Datetime()