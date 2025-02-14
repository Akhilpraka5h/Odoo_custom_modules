from odoo import api, fields, models
import json
from odoo.tools import json_default


class BookBorrowReport(models.TransientModel):
    """Report filter wizard"""
    _name = 'book.borrow.report'
    _description = 'Wizard for user to apply filters for library report'

    partner_id = fields.Many2one(comodel_name='res.partner')
    book_id = fields.Many2one(comodel_name='library.book',
                              domain="[('id', 'in', available_books_ids)]")
    checkout_date = fields.Datetime(string='Checkout Date')
    return_date = fields.Datetime(string='Return Date')
    book_genre_ids = fields.Many2many(comodel_name='book.genre')
    available_books_ids = fields.Many2many('library.book',
                                           compute="_compute_available_books")
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda
                                     self: self.env.user.company_id.id)
    date = fields.Datetime.now()

    @api.depends('partner_id')
    def _compute_available_books(self):
        for record in self:
            if record.partner_id:
                record.available_books_ids = self.env['library.book'].search([
                    ('borrower_ids.partner_id.id', '=', record.partner_id.id)
                ])
            else:
                record.available_books_ids = self.env['library.book'].search([])

    @api.model
    def create_data(self):
        passing_data = {
            'partner': self.partner_id.id,
            'book': self.book_id.id,
            'checkout_date': self.checkout_date,
            'return_date': self.return_date,
            'genre': self.book_genre_ids.ids,
            'filters': {'Member': self.partner_id.name,
                        'Book': self.book_id.book_title,
                        'Checkout': self.checkout_date,
                        'Return': self.return_date,
                        'Genres': ', '.join(
                            self.book_genre_ids.mapped('genre_name')),
                        'date': self.date
                        },
            'company': {
                'name': self.company_id.name,
                'street': self.company_id.street,
                'city': self.company_id.city,
                'state': self.company_id.state_id.code,
                'zip': self.company_id.zip,
                'country': self.company_id.country_id.name
            }
        }
        return passing_data

    def action_print_report(self):
        """Report print button action"""
        data = self.create_data()

        return self.env.ref(
            'library_management.action_report_book_checkout_line').report_action(
            None, data=data)

    def action_book_borrow_report_excel(self):
        """Button action to create xlsx report"""
        data = self.create_data()
        report_model = self.env[
            'report.library_management.book_checkout_line_report_template']
        report_data = report_model._get_report_values(None, data=data)
        data = report_data['data']

        return {
            'type': 'ir.actions.report',
            'data': {
                'model': 'report.library_management.book_checkout_line_report_template',
                'options': json.dumps(data, default=json_default),
                'output_format': 'xlsx',
                'report_name': 'Library Book History Report',
            },
            'report_type': 'xlsx',
        }
