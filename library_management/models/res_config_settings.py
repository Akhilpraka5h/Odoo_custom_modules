from odoo import fields, models


class LibrarySettings(models.TransientModel):
    """Library Management Setting"""
    _inherit = 'res.config.settings'

    max_borrow_day = fields.Integer(string='Maximum Borrowing Days',
                                    help='Maximum borrowing days for books',
                                    config_parameter='library_settings.max_borrow_day',
                                    default=10)
    reminder_day = fields.Integer(string='Reminder',
                                  help='Reminder days before a book is due',
                                  config_parameter='library_settings.reminder_day',
                                  default=2)
    penalty = fields.Float(string='Penalty',
                           help="Penalty charged for each hour a book is overdue",
                           config_parameter='library_settings.penalty')

    _sql_constraints = [
        ('check_max_borrow_day', 'CHECK(max_borrow_day >= 2)',
         "You cannot set a negative number for the default Maximum Borrowing Days."),
        ('check_reminder_day', 'CHECK(reminder_day >= 1)',
         "You cannot set a negative number for the default Reminder Days."),
        ('check_penalty', 'CHECK(penalty >= 0)',
         "You cannot set a negative number for the default Penalty."),
    ]
