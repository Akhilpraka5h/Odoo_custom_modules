from odoo import fields, models


class RecommendedBook(models.Model):
    """Recommendation for books"""
    _name = 'recommended.book'
    _description = 'Recommended Books'

    book_id = fields.Many2one(comodel_name='book.checkout', string='Book')
    book_borrower_id = fields.Many2one(comodel_name='res.partner',
                                       string='Borrower')
    recommended_books_ids = fields.One2many(comodel_name='recommendation',
                                            inverse_name='recommendation_id',
                                            string='Recommended Books',
                                            )

    def recommend_checkout_action(self):
        """Create a checkout draft entry for selected books."""
        selected_books = self.recommended_books_ids.filtered(
            lambda book: book.select_book)

        if selected_books:
            checkout_draft_books = self.env['library.book'].search([
                ('book_title', 'in', selected_books.mapped('book_title'))
            ])

            checkout_draft = self.book_id.create({
                'partner_name_id': self.book_borrower_id.id,
                'book_status': 'draft',
                'order_line_ids': [fields.Command.set(checkout_draft_books.ids)]
            })
            selected_books.write({
                'select_book': False,
            })
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'book.checkout',
                'view_mode': 'form',
                'res_id': checkout_draft.id
            }

        else:
            raise models.ValidationError(
                "Please select at least one book to proceed with checkout.")

    def recommend_close_action(self):
        """Clear selected books and close the recommendation."""
        selected_books = self.recommended_books_ids.filtered(
            lambda book: book.select_book)
        if selected_books:
            selected_books.write({
                'select_book': False,
            })
