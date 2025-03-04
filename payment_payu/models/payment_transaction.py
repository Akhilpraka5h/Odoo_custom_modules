import logging
import pprint
import hashlib
import json
from odoo import _, models
from odoo.exceptions import ValidationError
from odoo.addons.payment import utils as payment_utils
from werkzeug.urls import url_encode

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_processing_values(self, processing_values):
        """ Override of `payment` to return the Paypal-specific processing values.

        Note: self.ensure_one() from `_get_processing_values`

        :param dict processing_values: The generic and specific processing values of the
                                       transaction.
        :return: The dict of provider-specific processing values
        :rtype: dict
        """
        res = super()._get_specific_processing_values(processing_values)
        if self.provider_code != 'payu':
            return res

        partner_first_name, partner_last_name = payment_utils.split_partner_name(self.partner_name)

        hash_sequence = f"{self.provider_id.payu_merchant_key}|{self.reference}|{self.amount}|Odoo Payment|{partner_first_name}|{self.partner_email}|||||||||||{self.provider_id.payu_salt}"
        hashh = hashlib.sha512(hash_sequence.encode('utf-8')).hexdigest()

        payload = {
            'key': self.provider_id.payu_merchant_key,
            'txnid': self.reference,
            'amount': self.amount,
            'productinfo': 'Odoo Payment',
            'firstname': partner_first_name,
            'email': self.partner_email,
            'phone': self.partner_phone,
            'surl': self.provider_id.get_base_url() + '/payment/payu/success',
            'furl': self.provider_id.get_base_url() + '/payment/payu/failure',
            'hash': hashh,
        }

        # Construct PayU checkout URL
        payu_url = f"{self.provider_id.payu_api_url}/_payment"
        payment_url = f"{payu_url}?{url_encode(payload)}"

        _logger.info(
            "Redirecting transaction %s to PayU Checkout:\n%s",
            self.reference, payment_url
        )

        return {'redirect_url': payment_url}
