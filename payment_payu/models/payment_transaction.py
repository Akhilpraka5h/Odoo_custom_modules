import logging
import pprint
import hashlib
import json
import urllib
from werkzeug import urls
from odoo import _, models
from odoo.exceptions import ValidationError
from odoo.addons.payment import utils as payment_utils
from werkzeug.urls import url_encode
from odoo.addons.payment_payu.controllers.main import PayUController

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_processing_values(self, processing_values):
        """ Override of `payment` to return the Paypal-specific processing values.
        """
        res = super()._get_specific_processing_values(processing_values)
        if self.provider_code != 'payu':
            return res
        print(self.provider_id.payu_merchant_key)
        print(self.provider_id.payu_salt)

        partner_first_name, partner_last_name = payment_utils.split_partner_name(
            self.partner_name)

        hash_sequence = f"{self.provider_id.payu_merchant_key}|{self.reference}|{self.amount}|Odoo Payment|{partner_first_name}|{self.partner_email}|||||||||||{self.provider_id.payu_salt}"
        hashh = hashlib.sha512(hash_sequence.encode('utf-8')).hexdigest()

        payload = {
            'key': self.provider_id.payu_merchant_key,
            'txnid': self.reference,
            'amount': self.amount,
            'productinfo': 'OdooPayment',
            'firstname': partner_first_name,
            'email': self.partner_email,
            'phone': self.partner_phone,
            'surl': self.provider_id.get_base_url() + 'payment/success',
            'furl': self.provider_id.get_base_url() + 'payment/failure',
            'hash': hashh,
        }
        print('payload',payload)

        # Construct PayU checkout URL
        payu_url = "https://test.payu.in/_payment"
        payment_url = f"{payu_url}?{url_encode(payload)}"
        print('payment_url',payment_url)

        _logger.info(
            "Redirecting transaction %s to PayU Checkout:\n%s",
            self.reference, payment_url
        )

        return {'redirect_url': payment_url}

#
    def _get_specific_rendering_values(self, processing_values):
        """ Override of `payment` to return Mercado Pago-specific rendering values.
        """
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'payu':
            return res
        print('_get_specific_rendering_values')

        # Initiate the payment and retrieve the payment link data.
        payload = self._payu_prepare_preference_request_payload()

        encodedParams = urllib.parse.urlencode(payload)
        apiEndpoint = "https://test.payu.in/_payment"
        url = apiEndpoint + "?" + encodedParams

        rendering_values = {
            'api_url': apiEndpoint,
            'url_params': payload,  # Encore the params as inputs to preserve them.
        }
        return rendering_values
#
    def _payu_prepare_payment_request_payload(self):
        """ Create the payload for the payment request based on the transaction values.

        :return: The request payload
        :rtype: dict
        """
        print('_payu_prepare_payment_request_payload')
        base_url = self.provider_id.get_base_url()
        redirect_url = urls.url_join(base_url, PayUController._return_url)
        partner_first_name, partner_last_name = payment_utils.split_partner_name(
            self.partner_name)
        merchant_key = self.provider_id.payu_merchant_key
        transaction_id = self.reference
        amount = self.amount
        product_info = self.reference
        partner_firstname = partner_first_name
        partner_email = self.partner_email
        partner_phone = self.partner_phone
        success_url = redirect_url
        failure_url = base_url
        hash_sequence = f"{merchant_key}|{transaction_id}|{amount}|{product_info}|{partner_firstname}|{partner_email}|||||||||||{self.provider_id.payu_salt}"
        hash_value = hashlib.sha512(hash_sequence.encode('utf-8')).hexdigest()

        return {
            'key': merchant_key,
            'txnid': transaction_id,
            'amount': amount,
            'productinfo': product_info,
            'firstname': partner_firstname,
            'email': partner_email,
            'phone': partner_phone,
            'surl': success_url,
            'furl': failure_url,
            'hash': hash_value,
        }

