from odoo import api, fields, models


class BookAuthor(models.Model):
    """Book author"""
    _name = 'book.author'
    _description = 'Author'
    _rec_name = 'author_name_id'
    _inherit = ['mail.thread']

    author_name_id = fields.Many2one(comodel_name='res.partner', required=True,
                                     copy=False)
    author_desc = fields.Char(string='Biography')
    books_ids = fields.One2many(comodel_name='library.book',
                                inverse_name='book_author_id')
    book_count = fields.Integer(default=0, compute="_compute_book_count")

    @api.depends('books_ids')
    def _compute_book_count(self):
        """compute book count for the author"""
        self.book_count = len(self.books_ids)

    def action_books_record(self):
        """Smart button action"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Books',
            'view_mode': 'list,form',
            'res_model': 'library.book',
            'domain': [('book_author_id', '=', self.id)],
        }

    _sql_constraints = [
        ('author_name_id', 'UNIQUE(author_name_id)', 'Author already exist')
    ]
