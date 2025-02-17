from odoo import _, api, fields, models


class LibraryBooks(models.Model):
    """Books in the library"""
    _name = 'library.book'
    _description = 'Books'
    _rec_name = 'book_title'
    _inherit = ['mail.thread']

    book_title = fields.Char(string='Name', required=True)
    book_cover_image = fields.Image(string='Cover Image')
    book_id = fields.Char(readonly=True, string='ID',
                          default=lambda self: _('New'))
    isbn_id = fields.Char(string='ISBN')
    company_id = fields.Many2one('res.company', store=True,
                                 copy=False,
                                 string="Company",
                                 default=lambda
                                     self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    book_price = fields.Monetary(string='Price', default=1)
    book_cost = fields.Monetary(string='Cost', default=0)
    book_status = fields.Selection(
        selection=[
            ('coming_soon', 'Coming Soon'),
            ('available', 'Available'),
            ('unavailable', 'Unavailable')
        ],
        default='coming_soon',
        tracking=True
    )
    book_author_id = fields.Many2one(string='Author',
                                     comodel_name='book.author',
                                     required=True, context={'create': 'false'})
    book_publisher_id = fields.Many2one(string='Publisher',
                                        comodel_name='book.publisher',
                                        required=True,
                                        context={'create': 'false'})
    book_genre_ids = fields.Many2many(string='Genres',
                                      comodel_name='book.genre', store=True)
    borrower_ids = fields.One2many(string='Borrowers',
                                   comodel_name='book.checkout.line',
                                   inverse_name='book_checkout_id'
                                   )
    book_tag_ids = fields.Many2many(string='Tags', comodel_name='book.tag')
    book_publish_date = fields.Date(string='Published Date')
    checkout = fields.Boolean(string='Select', default=False)
    checkout_count = fields.Integer(default=0)
    borrow_count = fields.Integer(compute='_compute_book_borrow', store=True)
    image_attachment_ids = fields.Many2many('ir.attachment',
                                            string='Images')
    condition = fields.Selection(
        selection=[
            ('new', 'New'),
            ('good', 'Good'),
            ('old', 'Old')
        ]
    )
    description = fields.Char(string='Description')
    contributor_id = fields.Many2one(comodel_name='res.partner',
                                     string='Contributor')
    book_image_ids = fields.One2many(string='Book Extra Images',
                                     comodel_name='book.image',
                                     inverse_name='library_book_id')

    @api.depends('borrower_ids')
    def _compute_book_borrow(self):
        """Compute Borrowers count"""
        self.borrow_count = len(self.borrower_ids)

    @api.model_create_multi
    def create(self, vals):
        """Create Book"""
        for val in vals:
            val['book_id'] = self.env['ir.sequence'].next_by_code(
                'Book.Sequence') or _('New')
        return super(LibraryBooks, self).create(vals)

    def avail_action(self):
        """Set book as available"""
        self.book_status = 'available'

    def unavail_action(self):
        """Set book as unavailable"""
        self.book_status = 'unavailable'

    def action_view_borrowers(self):
        """Smart button action to open borrowers"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Borrowers',
            'view_mode': 'list,form',
            'res_model': 'book.checkout.line',
            'views': [
                (self.env.ref(
                    'library_management.book_checkout_line_library_book_view_list').id,
                 'list'),
                (self.env.ref(
                    'library_management.book_checkout_line_view_form_book').id,
                 'form')
            ],
            'domain': [('book_id', '=', self.id)],
        }

    _sql_constraints = [
        ('isbn_no', 'UNIQUE(isbn_id)', 'ISBN Number should be unique')
    ]
