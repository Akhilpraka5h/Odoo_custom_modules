# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class CommissionRevenueWise(models.Model):
    """Revenue wise Commission"""
    _name = 'commission.revenue.wise'
    _description = 'Revenue wise commission'

    sequence = fields.Char(string='Sequence', default=lambda self: _('New'))
    amount_from = fields.Monetary(string='Minimum Amount')
    amount_to = fields.Monetary(string='Maximum Amount')
    company_id = fields.Many2one('res.company', store=True,
                                 copy=False,
                                 string="Company",
                                 default=lambda
                                     self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    rate = fields.Float(string='Rate')
    commission_id = fields.Many2one(string='Commission',
                                    comodel_name='crm.commission')

    @api.model_create_multi
    def create(self, vals):
        """Create Book"""
        for val in vals:
            val['sequence'] = self.env['ir.sequence'].next_by_code(
                'revenue_sequence_code') or _('New')
        return super(CommissionRevenueWise, self).create(vals)
