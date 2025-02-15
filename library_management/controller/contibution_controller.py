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

    @http.route(['/Contributions', '/Contributions/page/<int:page>'], type='http', auth="user",
                website=True)
    def portal_book_contribution(self, search=None, search_in='All'):
        """To search the fleet vehicles data in the portal"""
        searchbar_inputs = {
            'All': {'label': 'All', 'input': 'All', 'domain': []},
            'Book Name': {'label': 'Book Name', 'input': 'Book Name',
                             'domain': [('book_title', 'like', search)]},
            'Author': {'label': 'Author',
                              'input': 'Author',
                              'domain': [('book_author_id.author_name_id.name', 'like', search)]},
            'Status': {'label': 'Status', 'input': 'Status',
                       'domain': [('condition', 'like', search)]},
        }
        search_domain = searchbar_inputs[search_in]['domain']
        books = request.env['library.book'].sudo().search([
            ('contributor_id', '=', request.env.user.partner_id.id)])
        search_book = books.search(search_domain)
        return request.render(
            'library_management.portal_my_home_book_contribution_views',
            {
                'books': search_book,
                'page_name': 'books',
                'search': search,
                'search_in': search_in,
                'searchbar_inputs': searchbar_inputs
            })