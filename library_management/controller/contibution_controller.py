from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal

class CustomPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'portal_contribution' in counters:
            values['portal_contribution'] = request.env[
                'library.book'].sudo().search_count([
                ('contributor_id', '=', request.env.user.partner_id.id),
            ])
        return values