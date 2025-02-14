from odoo import api, fields, models


class CommissionProductLine(models.Model):
    """To Add products, product category, Rate, Maximum commission in commission"""
    _name = 'commission.product.line'
    _description = 'Product line in commission'

    commission_id = fields.Many2one(comodel_name='crm.commission')
    product_id = fields.Many2one(comodel_name='product.product')
    product_categ_id = fields.Many2one(comodel_name='product.category')
    rate = fields.Float(string='Rate (%)')
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
    max_commission_amount = fields.Monetary(string='Maximum Commission Amount')

    rate_display = fields.Float(string="Rate (%)", default=0.05,
                                compute="_compute_rate_display",
                                inverse="_inverse_rate_display")

    @api.depends('rate')
    def _compute_rate_display(self):
        """To display percentage of Rate"""
        for record in self:
            record.rate_display = record.rate / 100

    def _inverse_rate_display(self):
        """To store rate percentage from UI"""
        for record in self:
            record.rate = record.rate_display * 100
