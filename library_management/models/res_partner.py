from odoo import fields, models


class ResPartner(models.Model):
    """Library Member details"""
    _inherit = 'res.partner'

    max_borrow_book = fields.Integer(string='Maximum Borrow', required=True,
                                     default=1,
                                     groups='library_management.group_librarian_user')
    max_late_return = fields.Integer(string='Maximum Late Return',
                                     required=True,
                                     default=3,
                                     groups='library_management.group_librarian_user')

    checkout_ids = fields.One2many(string='Books',
                                   comodel_name='book.checkout',
                                   inverse_name='partner_name_id')
    checkout_books_ids = fields.One2many(string='Books',
                                         comodel_name='book.checkout.line',
                                         inverse_name='partner_id')
    book_count = fields.Integer(string='Books', compute='_compute_book_count')


    def _compute_book_count(self):
        """To Display the book count"""
        self.book_count = len(self.checkout_books_ids)

    def action_get_books_record(self):
        """To open smart Button"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Books',
            'view_mode': 'list,form',
            'res_model': 'book.checkout.line',
            'views': [
                (self.env.ref(
                    'library_management.book_checkout_line_view_list_readonly').id,
                 'list'),
                (self.env.ref(
                    'library_management.book_checkout_line_view_form_readonly').id,
                 'form')
            ],
            'domain': [('partner_id', '=', self.id)],
            'context': {'create': False}
        }
