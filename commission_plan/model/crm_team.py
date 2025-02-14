from odoo import fields, models


class CrmTeam(models.Model):
    """Inherit Sales Team to add new field"""
    _inherit = 'crm.team'

    commission_id = fields.Many2one(string='Commission',
                                    comodel_name='crm.commission')
