from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    new_state = fields.Selection(
        selection=[
            ('open', 'Open'),
            ('close', 'Close')
        ],
        default='open',
        compute='_compute_check_quantity',
        readonly=False
    )
    close_selection = fields.Boolean()

    @api.depends('order_line')
    def _compute_check_quantity(self):
        total_qty = 0
        total_delivery = 0
        for order in self:
            total_qty = sum(order.order_line.mapped('product_uom_qty'))
            total_delivery = sum(order.order_line.mapped('qty_delivered'))
        if total_qty == total_delivery:
            self.new_state = 'close'
            self.close_selection = True
