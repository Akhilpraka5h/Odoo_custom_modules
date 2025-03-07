# -*- coding: utf-8 -*-
import logging
import pprint
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PayuController(http.Controller):
    _return_url = '/payment/payu/return'
    _webhook_url = '/payment/payu/webhook'

    @http.route(
        _return_url, type='http', auth='public', methods=['GET', 'POST'],
        csrf=False, save_session=False
    )
    def payu_return_from_checkout(self, **data):
        # _logger.info("handling redirection from Payu with data:\n%s",
        #              pprint.pformat(data))
        print('pprint.pformat(data)')
        # request.env['payment.transaction'].sudo()._handle_notification_data(
        #     'payu', data)
        return request.redirect('/payment/status')

    @http.route(_webhook_url, type='http', auth='public', methods=['POST'],
                csrf=False)
    def payu_webhook(self, **data):
        """ Process the notification data sent by Mollie to the webhook.
        """
        _logger.info("notification received from Payu with data:\n%s",
                     pprint.pformat(data))
        print('pprint.pformat(data)')
        try:
            request.env['payment.transaction'].sudo()._handle_notification_data(
                'payu', data)
        except ValidationError:  # Acknowledge the notification to avoid getting spammed
            _logger.exception(
                "unable to handle the notification data; skipping to acknowledge")
        return ''  # Acknowledge the notification
