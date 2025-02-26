from odoo import api, fields, models


class ResPartner(models.Model):
    """Inherit Partner to add Due Limit"""
    _name = 'res.partner'
    _inherit = ['res.partner', 'pos.load.mixin']

    due_limit = fields.Float(string='Due Limit')

    @api.model
    def _load_pos_data_fields(self, config_id):
        """Load newly created field"""
        data = super()._load_pos_data_fields(config_id)
        data.append('due_limit')
        return data
