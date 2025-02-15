from odoo.http import request, Controller, route


class BookSnippet(Controller):
    """Retrieve data from the backend and pass to the view"""

    @route(['/latest_library_books'], type="json", auth="user",
                website=True)
    def all_books(self):
        """Function to get all book from library"""
        print('controller working')
        books = request.env['library.book'].sudo().search_read(
            ['book_title', 'book_cover_image', 'id'],
            order='id asc')
        return books
