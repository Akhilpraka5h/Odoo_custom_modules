# -*- coding: utf-8 -*-
from odoo import fields, models


class SaleOrderLine(models.Model):
    """Inherit Sale order line"""
    _inherit = 'sale.order.line'

    categ_id = fields.Many2one(related='product_id.product_tmpl_id.categ_id')
    date_order = fields.Datetime(related='order_id.date_order')
