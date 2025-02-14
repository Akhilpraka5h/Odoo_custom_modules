from odoo import models


class ProductTemplate(models.Model):
    """Inherit product template"""
    _inherit = 'product.template'

    def quotation_action(self):
        product = self.env['product.product'].search(
            [('product_tmpl_id', '=', self.id)], limit=1)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Add To Quotation',
            'res_model': 'add.product.to.quotation',
            'target': 'new',
            'view_mode': 'form',
            'view_type': 'form',
            'context': {'default_product_id': product.id,
                        'default_product_template_id': self.id,
                        'default_list_price': self.list_price},
        }
