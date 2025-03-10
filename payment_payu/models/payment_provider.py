# -*- coding: utf-8 -*-

from odoo import fields, models


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('payu', 'payU')], ondelete={'payu': 'set default'}
    )
    payu_api_key = fields.Char(
        string="API Key",
        help="The Test or Live API Key depending on the configuration of the provider",
        required_if_provider="payu", groups="base.group_system"
    )
    payu_salt = fields.Char(
        string="Salt Code",
        required_if_provider="payu", groups="base.group_system"
    )

    def _get_default_payment_method_codes(self):
        """ Override of `payment` to return the default payment method codes. """
        default_codes = super()._get_default_payment_method_codes()
        if self.code != 'payu':
            return default_codes
        return {'card', 'visa', 'mastercard'}
