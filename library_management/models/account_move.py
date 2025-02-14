from  odoo import api, models


class AccountMove(models.Model):
    """inherit account move for invoice creation"""
    _inherit = 'account.move'

    @api.model
    def write(self, vals):
        """update book status to available once payment is complete"""
        res = super(AccountMove, self).write(vals)
        if self.payment_state == 'paid':
            if self.invoice_line_ids.book_id:
                for book in self.invoice_line_ids.book_id:
                    book.book_status = 'available'
        return res