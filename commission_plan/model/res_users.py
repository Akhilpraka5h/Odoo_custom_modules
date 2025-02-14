from odoo import api, fields, models


class ResUsers(models.Model):
    """Inherit salesperson to add commission"""
    _inherit = 'res.users'

    commission_id = fields.Many2one(comodel_name='crm.commission',
                                    domain="[('state','=','approved')]")
    company_id = fields.Many2one('res.company', store=True,
                                 copy=False,
                                 string="Company",
                                 default=lambda
                                     self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    commission = fields.Monetary(string='Commission',
                                 compute='_compute_salesperson_commission',
                                 store=True)

    @api.depends('commission_id')
    def _compute_salesperson_commission(self):
        for user in self:
            total_commission = 0
            sale_order_products = self.env['sale.order.line'].search(
                [('salesman_id', '=', user.id),
                 ('state', '=', 'sale'),
                 ('product_id', 'in',
                  user.commission_id.commission_product_ids.product_id.ids),
                 ('date_order', '>=', user.commission_id.date_from),
                 ('date_order', '<=', user.commission_id.date_to)
                 ])
            sale_order_category = self.env['sale.order.line'].search(
                [('salesman_id', '=', user.id),
                 ('state', '=', 'sale'),
                 ('categ_id', 'in',
                  user.commission_id.commission_product_ids.product_categ_id.ids),
                 ('date_order', '>=', user.commission_id.date_from),
                 ('date_order', '<=', user.commission_id.date_to)])

            commission_products = user.commission_id.commission_product_ids.product_id
            commission_categories = user.commission_id.commission_product_ids.product_categ_id

            if user.commission_id and user.commission_id.commission_type == 'product':
                for sale in sale_order_products:
                    sale_product = sale.product_id
                    sale_amount = sale.price_subtotal

                    for product in commission_products:
                        commission_product_line = user.commission_id.commission_product_ids.search(
                            [('product_id', '=', product.id),
                             ('commission_id', '=', user.commission_id.id)])
                        if product == sale_product:
                            rate = commission_product_line.rate / 100
                            max_amount = commission_product_line.max_commission_amount
                            commission = sale_amount * rate
                            if 0 < max_amount < commission:
                                commission = max_amount
                            total_commission += commission

                for sale in sale_order_category:
                    sale_category = sale.categ_id
                    sale_amount = sale.price_subtotal
                    for category in commission_categories:
                        commission_product_line = user.commission_id.commission_product_ids.search(
                            [('product_categ_id', '=', category.id),
                             ('commission_id', '=', user.commission_id.id)])
                        if category == sale_category:
                            rate = commission_product_line.rate / 100
                            max_amount = commission_product_line.max_commission_amount
                            commission = sale_amount * rate
                            if 0 < max_amount < commission:
                                commission = max_amount
                            total_commission += commission

            if user.commission_id and user.commission_id.commission_type == 'revenue':
                sale_order_lines = self.env['sale.order.line'].search([
                    ('salesman_id', '=', user.id),
                    ('state', '=', 'sale'),
                    ('date_order', '>=', user.commission_id.date_from),
                    ('date_order', '<=', user.commission_id.date_to)
                ])
                price_sum = 0
                rate = user.commission_id.rate / 100
                extra_rate = user.commission_id.extra_rate / 100

                for order_line in sale_order_lines:
                    price_sum += order_line.price_subtotal

                if (user.commission_id.revenue_type == 'straight' and
                        price_sum >= user.commission_id.amount_from):
                    total_commission = price_sum * rate

                elif (user.commission_id.revenue_type == 'gradual' and
                      price_sum >= user.commission_id.amount_from):
                    max_amount = user.commission_id.amount_to
                    after_max_amount = price_sum - max_amount
                    first_commission = 0
                    second_commission = 0
                    if price_sum >= max_amount:
                        first_commission = max_amount * rate
                        if after_max_amount > 0:
                            second_commission = after_max_amount * (
                                    rate + extra_rate)
                    total_commission = first_commission + second_commission

            user.commission = total_commission
