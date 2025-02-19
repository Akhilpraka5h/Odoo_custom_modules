from odoo.http import request, Controller, route
from odoo import fields


class BookSnippet(Controller):
    """Retrieve data from the backend and pass to the view"""

    @route(['/latest_library_books'], type="json", auth="user",
           website=True)
    def all_books(self):
        """Function to get all book from library"""
        current_website = request.env['website'].sudo().get_current_website()
        current_company = request.env.company
        company_currency = current_company.currency_id
        pricelist_currency = current_website.pricelist_id.currency_id
        currency_rate = request.env['res.currency']._get_conversion_rate(
            company_currency, pricelist_currency, current_company,
            fields.Date.today()) or 1.0

        books = request.env['library.book'].sudo().search_read([],
                                                               ['book_title',
                                                                'book_cover_image',
                                                                'id',
                                                                'borrow_count',
                                                                'book_price',
                                                                'book_status'],
                                                               order='borrow_count desc')

        for book in books:
            """get book price and covert them according to price-list"""
            book_price = book['book_price']
            converted_price = book_price * currency_rate
            book['converted_price'] = pricelist_currency.round(converted_price)

        return {'all_books': books,
                'website': current_website.id,
                'currency_symbol': pricelist_currency.symbol,
                'currency_position': pricelist_currency.position
                }
