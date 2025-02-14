from odoo import fields, models


class BookCheckoutLine(models.Model):
    """checkout order lines"""
    _name = 'book.checkout.line'
    _description = 'Checkout Lines'
    _rec_name = 'order_id'

    order_id = fields.Many2one(
        comodel_name='book.checkout',
        string="Order Reference")

    order_partner_id = fields.Many2one(
        related='order_id.partner_name_id',
        string="Member")
    book_id = fields.Many2one(
        comodel_name='library.book',
        string="Book",
        domain="[('book_status', '=', 'available')]",
        required=True)
    user_id = fields.Many2one(related='order_id.user_id')

    book_checkout_id = fields.Many2one(related='book_id')
    partner_id = fields.Many2one(related='order_id.partner_name_id')
    book_author_id = fields.Many2one(related='book_id.book_author_id')
    book_status = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('checked_out', 'Checked Out'),
            ('overdue', 'Overdue'),
            ('returned', 'Returned'),
            ('cancel', 'Cancelled')
        ],
        related='order_id.book_status'
    )
    checkout_date = fields.Datetime(string='Checkout Date', copy=False,
                                    related='order_id.checkout_date')
    due_date = fields.Datetime(string='Due date', copy=False,
                               related='order_id.due_date')
    return_date = fields.Datetime(string='Return Date', copy=False,
                                  related='order_id.return_date')

    book_return_status = fields.Selection(
        selection=[
            ('late', 'Late Return'),
            ('on_time', 'On Time Return'),
            ('draft', 'draft')
        ],
        compute='_compute_late_returns'
    )
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda
                                     self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    penalty = fields.Monetary(string='Penalty',
                              related='order_id.penalty')
    book_price = fields.Monetary(string='Price', related='book_id.book_price')
    each_book_penalty = fields.Monetary(string='Book Penalty',
                                        related='order_id.each_book_penalty')
    book_genre_ids = fields.Many2many(related='book_id.book_genre_ids')

    def _compute_late_returns(self):
        """Check the checkout return is late or on-time """
        for date in self:
            if date.return_date:
                if date.return_date > date.due_date:
                    date.book_return_status = 'late'
                else:
                    date.book_return_status = 'on_time'
            else:
                date.book_return_status = 'draft'
