# -*- coding: utf-8 -*-
import logging
import pprint

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)
class PayUController(http.Controller):
    _return_url = '/payment/payu/return'

    @http.route(
        _return_url, type='http', auth='public', methods=['GET', 'POST'], csrf=False,
        save_session=False
    )
    def mollie_return_from_checkout(self, **data):
        """ Process the notification data sent by Mollie after redirection from checkout.
        """
        # _logger.info("handling redirection from Mollie with data:\n%s", pprint.pformat(data))
        # request.env['payment.transaction'].sudo()._handle_notification_data('payu', data)
        return request.redirect('/payment/status')


# from odoo import http
# from odoo.exceptions import ValidationError
# from odoo.http import request
#
# class PayuController(http.Controller):
#     _return_url = '/payment/payu/return'
#
#     @http.route(
#         _return_url, type='http', auth='public', methods=['GET', 'POST'], csrf=False,
#         save_session=False
#     )
#     def payu_return_from_checkout(self, **data):
#         print('cat5')
#         # request.env['payment.transaction'].sudo()._handle_notification_data('payu', data)
#         return request.redirect('/payment/status')