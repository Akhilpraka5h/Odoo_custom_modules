from odoo import api, fields, models


class ProductProduct(models.Model):
    """Inherit Product model to add rating"""
    _inherit = 'product.product'

    rating = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    ],
        string='Rating',
        default='1',
        required=1)

    @api.model
    def _load_pos_data_fields(self, config_id):
        data = super()._load_pos_data_fields(config_id)
        data.append('rating')
        return data
