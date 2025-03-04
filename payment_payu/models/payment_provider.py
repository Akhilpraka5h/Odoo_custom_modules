# Part of Odoo. See LICENSE file for full copyright and licensing details.

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
    payu_api_url = fields.Char(
        string="PayU Api URL",
        required_if_provider='payu',
        groups='base.group_system',
    )

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

    def _paypal_get_inline_form_values(self, currency=None):
        """ Return a serialized JSON of the required values to render the inline form.

        Note: `self.ensure_one()`

        :param res.currency currency: The transaction currency.
        :return: The JSON serial of the required values to render the inline form.
        :rtype: str
        """
        inline_form_values = {
            'provider_id': self.id,
            'merchant_key': self.payu_merchant_key,
            'currency_code': currency and currency.name,
        }
        return json.dumps(inline_form_values)
