from odoo import api, fields, models
from odoo.exceptions import UserError


class CrmCommission(models.Model):
    """Commission plan for salesperson"""
    _name = 'crm.commission'
    _description = 'Commission plan for salesperson'
    _inherit = ['mail.thread']

    name = fields.Char(string='Name', required=True, copy=False)
    date_from = fields.Datetime(string='From', required=True)
    date_to = fields.Datetime(string='To', required=True)
    commission_type = fields.Selection(
        selection=[
            ('product', 'Product wise'),
            ('revenue', 'Revenue wise')
        ],
        string='Type',
        default='product',
        required=True
    )
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda
                                     self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    commission_product_ids = fields.One2many(
        comodel_name='commission.product.line',
        inverse_name='commission_id')

    revenue_type = fields.Selection(
        selection=[
            ('straight', 'Straight'),
            ('gradual', 'Graduated')
        ],
        string='Type',
        default='straight',
        required=True,
        copy=False
    )
    rate = fields.Float(string='Rate (%)')
    amount_from = fields.Monetary(string='Minimum Amount', copy=False)
    amount_to = fields.Monetary(string='Maximum Amount', copy=False)
    extra_rate = fields.Float(string='Extra (%)', copy=False)
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('approved', 'Approved'),
            ('done', 'Done'),
            ('cancel', 'Cancelled'),
        ],
        default='draft',
        required=True,
        copy=False
    )
    revenue_wise_ids = fields.One2many(comodel_name='commission.revenue.wise',
                                       inverse_name='commission_id')
    rate_display = fields.Float(string="Rate (%)", default=0.05,
                                compute="_compute_rate_display",
                                inverse="_inverse_rate_display")
    extra_rate_display = fields.Float(string="Extra Rate (%)", default=0.01,
                                      compute="_compute_rate_display",
                                      inverse="_inverse_rate_display")

    @api.constrains('amount_from', 'amount_to')
    def _check_amount(self):
        """To check the minimum and maximum amount"""
        if self.amount_from or self.amount_to:
            if self.amount_from > self.amount_to:
                raise UserError(
                    "Maximum amount should be greater than Minimum amount")

    @api.depends('rate', 'extra_rate')
    def _compute_rate_display(self):
        """To display percentage of Rate"""
        for record in self:
            record.rate_display = record.rate / 100
            record.extra_rate_display = record.extra_rate / 100

    def _inverse_rate_display(self):
        """To store rate percentage from UI"""
        for record in self:
            record.rate = record.rate_display * 100
            record.extra_rate = record.extra_rate_display * 100

    def action_approve(self):
        """Approve Button action"""
        self.state = 'approved'

    def action_cancel(self):
        """Cancel Button action"""
        self.state = 'cancel'

    def action_done(self):
        """Done Button action"""
        self.state = 'done'

    def action_draft(self):
        """Reset to draft Button action"""
        self.state = 'draft'

    _sql_constraints = [
        ('commission_name', 'unique (name)',
         "The Commission plan name Already exist.")
    ]
