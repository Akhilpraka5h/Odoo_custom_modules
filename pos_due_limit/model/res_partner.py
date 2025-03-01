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
                used_credit = self.env['pos.order'].search([
                    ('partner_id', '=', partner.id),
                    ('state', 'in', ['paid', 'done', 'invoiced']),
                    ('payment_ids.payment_method_id.name', '=',
                     'Customer Account')
                ]).mapped('amount_total')
                paid_amount = self.env['pos.order'].search([
                    ('partner_id', '=', partner.id),
                    ('state', 'in', ['paid', 'done', 'invoiced']),
                    ('payment_ids.payment_method_id.name', '=',
                     'Customer Account'),
                    ('account_move.payment_state', '=', 'paid')
                ]).mapped('amount_total')
                partner.credit_used = sum(used_credit) - sum(paid_amount)

    @api.depends('credit_limit', 'credit_used')
    def _compute_credit_available(self):
        for partner in self:
            partner.credit_balance = round(
                (partner.credit_limit - partner.credit_used), 2)

    @api.model
    def _load_pos_data_fields(self, config_id):
        """Load newly created field"""
        data = super()._load_pos_data_fields(config_id)
        data += ['credit_limit', 'credit_used', 'credit_balance']
        return data
