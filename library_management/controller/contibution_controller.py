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

    @http.route(['/Contributions'], type='http', auth="user", website=True)
    def portal_book_contribution(self):
        books = request.env['library.book'].sudo().search([
            ('contributor_id', '=', request.env.user.partner_id.id)
        ])
        return request.render(
            'library_management.portal_my_home_book_contribution_views',
            {'books': books, 'page_name': 'books'}
        )