# -*- coding: utf-8 -*-
from odoo import models


class ProductProduct(models.Model):
    """Inherit product template"""
    _inherit = 'product.product'

    def quotation_action(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Add To Quotation',
            'res_model': 'add.product.to.quotation',
            'target': 'new',
            'view_mode': 'form',
            'view_type': 'form',
            'context': {'default_product_id': self.id,
                        'default_list_price': self.lst_price},
        }
