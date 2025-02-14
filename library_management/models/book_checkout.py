from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError
from odoo.tools import date_utils


class BookCheckout(models.Model):
    """Book checkout"""
    _name = 'book.checkout'
    _description = 'Checkout'
    _rec_name = 'checkout_id'
    _inherit = ['mail.thread']

    partner_name_id = fields.Many2one(comodel_name='res.partner',
                                      string='Borrower by', required=True,
                                      domain="[('is_company', '=', False)]")
    partner_phone = fields.Char(string='Phone', related='partner_name_id.phone')
    today_date = fields.Datetime.now()
    checkout_date = fields.Datetime(string='Checkout Date', copy=False)
    due_date = fields.Datetime(string='Due date', copy=False)
    return_date = fields.Datetime(string='Return Date', copy=False)
    book_status = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('checked_out', 'Checked Out'),
            ('overdue', 'Overdue'),
            ('returned', 'Returned'),
            ('cancel', 'Cancelled')
        ],
        string='Status',
        default='draft',
        required=True,
        tracking=True,
        copy=False
    )
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda
                                     self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    penalty = fields.Monetary(string='Penalty', copy=False)
    user_id = fields.Many2one(comodel_name='res.users', string='Salesperson',
                              index=True, tracking=True,
                              default=lambda self: self.env.user)
    order_line_ids = fields.One2many(
        comodel_name='book.checkout.line',
        inverse_name='order_id',
        string="Order Lines",
        copy=True, required=True,
        ondelete="cascade")
    book_author_id = fields.Many2one(
        related='order_line_ids.book_id.book_author_id')
    book_genre_ids = fields.Many2many(
        related='order_line_ids.book_id.book_genre_ids')
    checkout_id = fields.Char(readonly=True, string='ID',
                              default=lambda self: _('New'))
    suggestion_ids = fields.One2many(comodel_name='recommendation',
                                     inverse_name='checkout_id')
    maximum_book_checkout = fields.Integer(
        related='partner_name_id.max_borrow_book')
    maximum_late_return = fields.Integer(
        related='partner_name_id.max_late_return'
    )
    each_book_penalty = fields.Monetary(string='Penalty')
    return_status = fields.Selection(selection=[
        ('draft', 'draft'),
        ('late_return', 'Late Return'),
        ('on_time', 'On time return')
    ],
        default='draft')
    invoice_id = fields.Many2one(comodel_name='account.move')
    invoice_count = fields.Integer(string='Invoice Count')

    @api.model_create_multi
    def create(self, vals):
        """Create checkout sequence"""
        for val in vals:
            val['checkout_id'] = self.env['ir.sequence'].next_by_code(
                'Checkout.Sequence')or _('New')
        return super(BookCheckout, self).create(vals)

    @api.onchange('partner_name_id')
    def partner_warning(self):
        late_returns = len(self.partner_name_id.checkout_ids.filtered(
            lambda book: book.return_status == 'late_return'))
        if self.partner_name_id:
            if late_returns >= self.maximum_late_return:
                return {'warning': {
                    'title': _('Warning'),
                    'message': _(
                        '"%s" has late returns',
                        self.partner_name_id.name)}}

    def checkout_action(self):
        """Create book checkout action"""
        setting_borrow_days = (
            self.env['ir.config_parameter']
            .sudo().get_param('library_settings.max_borrow_day'))
        default_borrow_days = int(setting_borrow_days)

        partner_checkout_status_list = self.partner_name_id.checkout_ids.mapped(
            'book_status')
        partner_book_checkout_count = self.env['library.book'].search_count([
            ('borrower_ids.partner_id.id', '=', self.partner_name_id.id),
            ('borrower_ids.book_status', '=', 'checked_out')
        ])
        order_line_count = len(self.order_line_ids.ids)
        late_returns = len(self.partner_name_id.checkout_ids.filtered(
            lambda book: book.return_status == 'late_return'))

        for date in self:
            if date.book_status == 'draft':
                all_books_available = all(
                    book.book_status == 'available' for book in
                    date.order_line_ids.book_id)
                if (
                        partner_book_checkout_count + order_line_count) > date.maximum_book_checkout:
                    raise ValidationError(
                        "You have reached your maximum checkout. Please "
                        "return the books or reduce the books from the current checkout")
                if 'overdue' in partner_checkout_status_list:
                    raise ValidationError(
                        "You have an overdue. Please return the book for new "
                        "checkout")
                if late_returns >= date.maximum_late_return:
                    raise ValidationError(
                        "You have reached your maximum late returns.")

                if all_books_available:
                    date.book_status = 'checked_out'
                    date.checkout_date = fields.Datetime.now()
                    for book in date.order_line_ids.book_id:
                        book.book_status = 'unavailable'
                    date.order_line_ids = [(4, book.id) for book in
                                           date.order_line_ids]

                    if not date.due_date:
                        date.due_date = date_utils.add(date.checkout_date,
                                                       days=default_borrow_days)

                    if date.order_line_ids:
                        recommended_books = self.env['library.book'].search([
                            '|', '|',
                            ('book_author_id', '=', self.book_author_id.id),
                            ('book_genre_ids', 'in', self.book_genre_ids.ids),
                            ('checkout_count', '>', 5),
                            ('book_status', '=', 'available')
                        ],
                            limit=5).filtered(
                            lambda
                                book: book.id != date.order_line_ids.book_id.ids)
                        for book in recommended_books:
                            self.env['recommendation'].create([{
                                'book_title': book.book_title,
                                'book_cover_image': book.book_cover_image,
                                'checkout_id': self.id
                            }])
                else:
                    raise ValidationError(
                        "One or more books are currently unavailable.")

    def return_action(self):
        """Return checkout book action"""
        setting_penalty = (
            self.env['ir.config_parameter']
            .sudo().get_param('library_settings.penalty'))

        if setting_penalty:
            default_penalty_hourly = float(setting_penalty)
        else:
            default_penalty_hourly = 0.0

        recommended_books = self.env['recommendation'].search([
            ('checkout_id', '=', self.id)
        ])
        order_line_count = len(self.order_line_ids.ids)

        for record in self:
            if record.book_status != 'returned':
                record.book_status = 'returned'

                if not record.return_date:
                    record.return_date = fields.Datetime.now()
                if record.return_date and record.checkout_date:
                    elapsed_time = record.return_date - record.due_date
                    hours_elapsed = elapsed_time.total_seconds() / 3600
                    if hours_elapsed > 0:
                        record.penalty = hours_elapsed * default_penalty_hourly
                        record.each_book_penalty = record.penalty / order_line_count
                        record.return_status = 'late_return'
                    else:
                        record.penalty = 0.0
                        record.return_status = 'on_time'

                    recommendation = self.env['recommended.book'].create([{
                        'book_id': record.id,
                        'book_borrower_id': record.partner_name_id.id,
                        'recommended_books_ids': [
                            fields.Command.set(recommended_books.ids)]
                    }])

                    return {
                        'type': 'ir.actions.act_window',
                        'name': _('Recommended Books'),
                        'res_model': 'recommended.book',
                        'res_id': recommendation.id,
                        'target': 'new',
                        'view_mode': 'form',
                    }

                else:
                    raise ValidationError(
                        "Return date or checkout date is not defined.")

            else:
                raise ValidationError(
                    "Action can't be performed on already returned checkouts.")

    def due_action(self):
        """Change to due state"""
        for date in self:
            if date.book_status != 'returned':
                date.book_status = 'overdue'
                notice_template = self.env.ref(
                    'library_management.overdue_email_template')
                notice_template.send_mail(self.id, force_send=True)
            else:
                raise ValidationError("Action can't perform for Returned Books")

    def cancel_action(self):
        """Cancel the checkout and reset status to draft"""
        for record in self:
            record.book_status = 'cancel'

            for book in record.order_line_ids.book_id:
                book.book_status = 'available'

    @api.constrains('due_date', 'return_date', 'checkout_date')
    def _check_dates(self):
        """Check due_date and return_date are not earlier than checkout_date."""
        for record in self:
            if (record.due_date and record.checkout_date and
                    record.due_date < record.checkout_date):
                raise ValidationError(
                    "The due date cannot be earlier than the checkout date.")
            if record.return_date and record.checkout_date and record.return_date < record.checkout_date:
                raise ValidationError(
                    "The return date cannot be earlier than the checkout date.")
            if not record.order_line_ids:
                raise UserError(
                    "Add a Book"
                )

    @api.model
    def _send_reminder_action(self):
        """Send reminder and overdue notices on time"""
        setting_reminder_days = (
            self.env['ir.config_parameter']
            .sudo().get_param('library_settings.reminder_day'))

        default_reminder_days = int(
            setting_reminder_days) if setting_reminder_days else 0
        for record in self.search([('book_status', '=', 'checked_out')]):
            if record.checkout_date and record.due_date:
                remaining_days = (record.due_date - record.checkout_date).days
                if remaining_days == default_reminder_days:
                    template = self.env.ref(
                        'library_management.reminder_email_template')
                    template.send_mail(record.id, force_send=True)

                if record.today_date > record.due_date:
                    record.book_status = 'overdue'
                    notice_template = self.env.ref(
                        'library_management.overdue_email_template')
                    notice_template.send_mail(record.id, force_send=True)

    def invoice_action(self):
        """create invoice button action"""
        invoice = self.env['account.move'].create([{
            'move_type': 'out_invoice',
            'partner_id': self.partner_name_id.id,
            'invoice_date': fields.Datetime.now(),
            'delivery_date': fields.Datetime.now(),
            'invoice_line_ids': [fields.Command.create({
                'quantity': 1,
                'product_id': self.env.ref(
                    'library_management.book_product'
                ).id,
                'book_id': book.book_id.id,
                'name': book.book_id.book_title,
                'price_unit': book.book_id.book_price
            }) for book in self.order_line_ids],
        }])
        if self.penalty:
            invoice.write({
                'invoice_line_ids': [fields.Command.create({
                    'quantity': 1,
                    'product_id': self.env.ref(
                        'library_management.late_return_product'
                    ).id,
                    'name': 'Late return',
                    'price_unit': self.penalty
                })]
            })
        self.invoice_count +=1
        self.invoice_id = invoice
        return {
            'type': 'ir.actions.act_window',
            'name': 'Checkout Invoice',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': self.invoice_id.id
        }
    def action_view_checkout_invoice(self):
        """Smart button action for invoice """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Checkout Invoice',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': self.invoice_id.id,
            'context': {'create': False}
        }
