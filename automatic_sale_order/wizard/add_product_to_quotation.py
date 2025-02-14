from odoo import api, fields, models, Command


class AddProductToQuotation(models.TransientModel):
    """From this wizard the product is added to Quotation,
     if open quotation is exist for partner else create new quotation"""
    _name = 'add.product.to.quotation'
    _description = 'Add product to quotation for the partner'

    partner_id = fields.Many2one(comodel_name='res.partner', required=True)
    product_id = fields.Many2one(comodel_name='product.product')
    product_uom_qty = fields.Float(default=1, required=True)
    list_price = fields.Float()
    product_amount = fields.Float(compute='_compute_product_amount', store=True)
    product_template_id = fields.Many2one(comodel_name='product.template')
    company_id = fields.Many2one('res.company', store=True,
                                 copy=False,
                                 string="Company",
                                 default=lambda
                                     self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency',
                                  string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)

    @api.depends('product_uom_qty', 'list_price')
    def _compute_product_amount(self):
        self.product_amount = self.list_price * self.product_uom_qty

    def add_to_quotation(self):
        open_quotation = self.env['sale.order'].search([
            ('partner_id', '=', self.partner_id.id),
            ('state', 'in', ('draft', 'sent'))
        ], limit=1)

        if open_quotation:
            open_quotation.write({
                'order_line': [Command.create({
                    'product_id': self.product_id.id,
                    'product_uom_qty': self.product_uom_qty,
                    'price_unit': self.list_price
                })]
            })
        else:
            open_quotation = self.env['sale.order'].create([{
                'partner_id': self.partner_id.id,
                'order_line': [Command.create({
                    'product_id': self.product_id.id,
                    'product_uom_qty': self.product_uom_qty,
                    'price_unit': self.list_price
                })]
            }])
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Order',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': open_quotation.id
        }
