# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResPartner(models.Model):
    """Inherit Partner to add Due Limit"""
    _inherit = 'res.partner'

    credit_limit = fields.Float(string='Credit Limit')
    credit_used = fields.Float(string='Credit Used',
                               compute='_compute_credit_used', store=True)
    credit_balance = fields.Float(string='Credit Balance',
                                  compute='_compute_credit_balance')

    @api.depends('pos_order_ids.amount_total', 'pos_order_ids.state',
                 'pos_order_ids.account_move.payment_state', 'credit_limit')
    def _compute_credit_used(self):
        """For Compute used credit for the partner"""
        for partner in self:
            self.credit_used = 0.0
            if partner.credit_limit:
                pos_orders = self.env['pos.order'].search([
                    ('partner_id', '=', partner.id),
                    ('state', 'in', ['paid', 'done', 'invoiced'])
                ])

                credit_payment = 0.0
                paid_credit_payment = 0.0
                for order in pos_orders:
                    """Total amount paid using customer account"""
                    for payment in order.payment_ids.filtered(
                            lambda t: t.payment_method_id.name == 'Customer Account'):
                        credit_payment += payment.amount

                    """Total payment amount for customer account"""
                    if order.account_move and order.account_move.payment_state == 'paid':
                        for payment in order.payment_ids.filtered(
                                lambda t: t.payment_method_id.name == 'Customer Account'):
                            paid_credit_payment += payment.amount

                partner.credit_used = credit_payment - paid_credit_payment  # total credit used by the customer

    @api.depends('credit_limit', 'credit_used')
    def _compute_credit_balance(self):
        """For Compute available credit for the partner"""
        for partner in self:
            partner.credit_balance = round(
                (partner.credit_limit - partner.credit_used), 2)

    @api.model
    def _load_pos_data_fields(self, config_id):
        """Load newly created field"""
        data = super()._load_pos_data_fields(config_id)
        data += ['credit_limit', 'credit_used', 'credit_balance']
        return data
