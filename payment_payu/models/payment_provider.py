# -*- coding: utf-8 -*-

import requests
from odoo.exceptions import ValidationError
# from werkzeug import urls

from odoo import _, fields, models


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('payu', 'payU')], ondelete={'payu': 'set default'}
    )
    payu_api_key = fields.Char(
        string="PayU API Key",
        help="The Test or Live API Key depending on the configuration of the provider",
        required_if_provider="payu", groups="base.group_system"
    )
    payu_salt = fields.Char(
        string="Payu Salt Code",
        required_if_provider="payu", groups="base.group_system"
    )

    def _get_default_payment_method_codes(self):
        """ Override of `payment` to return the default payment method codes. """
        default_codes = super()._get_default_payment_method_codes()
        if self.code != 'payu':
            return default_codes
        return {'ideal', 'amex', 'card', 'discover', 'visa', 'mastercard'}

    def _payu_make_request(self, endpoint, data=None, method='POST'):
        self.ensure_one()
        headers = {"Accept": "application/json",
                   "Content-Type": "application/x-www-form-urlencoded"}
        url = "https://test.payu.in/_payment"
        try:
            response = requests.request("POST", url, data=data, headers=headers,
                                        timeout=10)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                raise ValidationError(
                    "Mollie: " + _(
                        "The communication with the API failed. Mollie gave us the following "
                        "information: %s", response.json().get('detail', '')
                    ))
        except (
        requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            raise ValidationError(
                "Mollie: " + _("Could not establish the connection to the API.")
            )
        return ''
