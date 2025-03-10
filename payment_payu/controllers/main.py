# -*- coding: utf-8 -*-
import logging
import pprint
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class PayuController(http.Controller):
    _return_url = '/payment/payu/return'

    @http.route(
        _return_url, type='http', auth='public', methods=['GET', 'POST'],
        csrf=False, save_session=False
    )
    def payu_return_from_checkout(self, **data):
        """ Process the notification data sent by Payu after redirection from checkout.
                :param dict data: The notification data.
                """
        _logger.info("handling redirection from Payu with data:\n%s",
                     pprint.pformat(data))
        request.env['payment.transaction'].sudo()._handle_notification_data(
            'payu', data)
        return request.redirect('/payment/status')
