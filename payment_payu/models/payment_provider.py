# -*- coding: utf-8 -*-

import hashlib
import hmac
import logging
import pprint
import json
import requests

from odoo import _, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('payu', "PayU")], ondelete={'payu': 'set default'}
    )
    payu_merchant_key = fields.Char(
        string="PayU Merchant Key",
        required_if_provider='payu',
        groups='base.group_system',
    )
    payu_salt = fields.Char(
        string="PayU Salt",
        required_if_provider='payu',
        groups='base.group_system',
    )

    def _payu_make_request(self, endpoint, data=None, method='POST'):
        """ Make a request at Payu endpoint."""

        self.ensure_one()
        url = f'https://test.payu.in/_payment/{endpoint}'
        print('haii')

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        try:
            response = requests.request(method, url, json=data, headers=headers, timeout=10)
            print('response')
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                _logger.exception(
                    "Invalid API request at %s with data:\n%s", url, pprint.pformat(data)
                )
                raise ValidationError(
                    "Mollie: " + _(
                        "The communication with the API failed. Mollie gave us the following "
                        "information: %s", response.json().get('detail', '')
                    ))
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            _logger.exception("Unable to reach endpoint at %s", url)
            raise ValidationError(
                "Mollie: " + _("Could not establish the connection to the API.")
            )
        return response.json()

    def _get_default_payment_method_codes(self):
        """ Override of `payment` to return the default payment method codes. """
        default_codes = super()._get_default_payment_method_codes()
        if self.code != 'payu':
            return default_codes
        return {
            # Primary payment methods.
            'card',
            # Brand payment methods.
            'visa',
            'mastercard',
            'amex',
            'discover',
        }
