from odoo.http import request, Controller, route


class BookSnippet(Controller):
    """Retrieve data from the backend and pass to the view"""

    @route(['/latest_library_books'], type="json", auth="user",
           website=True)
    def all_books(self):
        """Function to get all book from library"""
        current_website = request.env['website'].sudo().get_current_website()
        current_company = request.env.company
        company_currency = current_company.currency_id
        currency_symbol = company_currency.symbol
        pricelist_currency = current_website.pricelist_id.currency_id
        pricelist_cur_symbol = pricelist_currency.symbol
        books = request.env['library.book'].sudo().search_read([],
                                                               ['book_title',
                                                                'book_cover_image',
                                                                'id',
                                                                'borrow_count',
                                                                'book_price',
                                                                'book_status',
                                                                'currency_id',
                                                                'company_id'],
                                                               order='borrow_count desc')
        currency_data = request.env['res.currency'].sudo().browse(pricelist_currency.id).read(
                                                       ['name',
                                                        'symbol',
                                                        'rounding',
                                                        'decimal_places',
                                                        'position'])
        currency_rate = request.env['res.currency.rate'].sudo().search_read([('currency_id','=',pricelist_currency.id)],[
            'id','company_rate'],limit=1,order='id desc')
# got needed data for price calculation need to calculate and display
        print('pricelist_id',pricelist_currency.symbol)
        print('currency_data',currency_data)
        print('pricelist_currency.id',pricelist_currency.id)
        print('currency_rate',currency_rate)
        return {'all_books': books,
                'website': current_website.id,
                'currency': currency_symbol if company_currency.id == pricelist_currency.id else pricelist_cur_symbol }
