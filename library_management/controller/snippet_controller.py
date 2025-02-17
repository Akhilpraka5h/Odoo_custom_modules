from odoo.http import request, Controller, route
from odoo.tools.safe_eval import time


class BookSnippet(Controller):
    """Retrieve data from the backend and pass to the view"""

    @route(['/latest_library_books'], type="json", auth="user",
           website=True)
    def all_books(self):
        """Function to get all book from library"""
        current_website = request.env['website'].sudo().get_current_website().id
        books = request.env['library.book'].sudo().search_read([],
                                                               ['book_title',
                                                                'book_cover_image',
                                                                'id',
                                                                'borrow_count',
                                                                'book_price',
                                                                'book_status'],
                                                               order='borrow_count desc')
        unique_id = "pc-%d" % int(time.time() * 1000)
        return {'all_books': books,
                'website': current_website,
                'unique_id': unique_id}
