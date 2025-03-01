from odoo import api, fields, models


class ResPartner(models.Model):
    """Inherit Partner to add Due Limit"""
    _inherit = 'res.partner'

    credit_limit = fields.Float(string='Credit Limit')
    credit_used = fields.Float(string='Credit Used',
                               compute='_compute_credit_used', store=True)
    credit_balance = fields.Float(string='Credit Balance',
                                  compute='_compute_credit_available')

    @api.depends('pos_order_ids.amount_total', 'pos_order_ids.state',
                 'pos_order_ids.account_move.payment_state', 'credit_limit')
    def _compute_credit_used(self):
        self.credit_used = 0.0
        for partner in self:
            if partner.credit_limit:
                pos_orders = self.env['pos.order'].search([
                    ('partner_id', '=', partner.id),
                    ('state', 'in', ['paid', 'done', 'invoiced'])
                ])
                credit_payment = 0.0
                paid_credit_payment = 0.0
                for order in pos_orders:
                    for payment in order.payment_ids:
                        if payment.payment_method_id.name == 'Customer Account':
                            credit_payment += payment.amount
                print(credit_payment)
                for order in pos_orders:
                    if order.account_move and order.account_move.payment_state == 'paid':
                        for payment in order.payment_ids:
                            if payment.payment_method_id.name == 'Customer Account':
                                paid_credit_payment += payment.amount
                print(paid_credit_payment)
                print('credit amount', (credit_payment - paid_credit_payment))
                partner.credit_used = credit_payment - paid_credit_payment

    @api.depends('credit_limit', 'credit_used')
    def _compute_credit_available(self):
        for partner in self:
            partner.credit_balance = round(
                (partner.credit_limit - partner.credit_used), 2)
            #
            # if partner.credit_limit:
            #     pos_orders = self.env['pos.order'].search([
            #         ('partner_id', '=', partner.id),
            #         ('state', 'in', ['paid', 'done', 'invoiced'])
            #     ])
            # credit_payment = 0.0
            # paid_credit_payment = 0.0
            # for order in pos_orders:
            #     for payment in order.payment_ids:
            #         if payment.payment_method_id.name == 'Customer Account':
            #             credit_payment += payment.amount
            # print(credit_payment)
            # for order in pos_orders:
            #     if order.account_move and order.account_move.payment_state == 'paid':
            #         for payment in order.payment_ids:
            #             if payment.payment_method_id.name == 'Customer Account':
            #                 paid_credit_payment += payment.amount
            # print(paid_credit_payment)
            # print('credit amount', (credit_payment - paid_credit_payment))

    @api.model
    def _load_pos_data_fields(self, config_id):
        """Load newly created field"""
        data = super()._load_pos_data_fields(config_id)
        data += ['credit_limit', 'credit_used', 'credit_balance']
        return data
