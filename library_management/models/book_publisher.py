from odoo import api, fields, models


class BookPublisher(models.Model):
    """Book Publisher"""
    _name = 'book.publisher'
    _description = 'Publisher'
    _inherit = ['mail.thread']
    _rec_name = 'publisher_name_id'

    publisher_name_id = fields.Many2one(comodel_name='res.partner',
                                        required=True, copy=False)
    add_street = fields.Char(string='Street',
                             related='publisher_name_id.street')
    add_street_2 = fields.Char(string='Street 2',
                               related='publisher_name_id.street2')
    add_city = fields.Char(string='City', related='publisher_name_id.city')
    add_state_id = fields.Many2one(string='State',
                                   related='publisher_name_id.state_id')
    add_country_code = fields.Char(string='Country',
                                   related='publisher_name_id.country_code')

    books_ids = fields.One2many(comodel_name='library.book',
                                inverse_name='book_publisher_id')
    book_count = fields.Integer(default=0, compute="_compute_book_count")

    @api.depends('books_ids')
    def _compute_book_count(self):
        """Compute book count"""
        self.book_count = len(self.books_ids)

    def action_books_record(self):
        """Smart button action"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Books',
            'view_mode': 'list,form',
            'res_model': 'library.book',
            'domain': [('book_publisher_id', '=', self.id)],
        }

    _sql_constraints = [
        ('publisher_name_id', 'UNIQUE(publisher_name_id)',
         'Publisher already exist')
    ]
