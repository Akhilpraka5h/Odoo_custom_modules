# -*- coding: utf-8 -*-

from odoo import _, fields, models
from werkzeug import urls
from odoo.addons.payment_payu.controllers.main import PayuController
from odoo.exceptions import ValidationError
import hashlib
import pprint
import logging

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'payu':
            return res
        payload = self._payu_prepare_payment_request_payload()
        _logger.info("sending '/payments' request for link creation:\n%s",
                     pprint.pformat(payload))
        api_url = 'https://test.payu.in/_payment'
        return {'api_url': api_url,
                'url_params': payload}

    def _payu_prepare_payment_request_payload(self):
        # Payment gateways work in https for ensuring security.
        # So using NGROK by replacing the localhost with url. Check NGROK for more INFO
        base_url = "https://fb39-103-139-64-225.ngrok-free.app"
        redirect_url = urls.url_join(base_url, PayuController._return_url)
        key = self.provider_id.payu_api_key
        txnid = (f'{self.reference}{fields.datetime.now()}').replace(' ', '_')
        productinfo = self.reference
        amount = self.amount
        email = self.partner_email
        firstname = self.partner_name
        surl = redirect_url
        furl = redirect_url
        phone = self.partner_phone
        salt = self.provider_id.payu_salt
        hash_value = hashlib.sha512(
            f"{key}|{txnid}|{amount}|{productinfo}|{firstname}|{email}|||||||||||{salt}".encode(
                'utf-8')).hexdigest()
        return {
            'key': key,
            'txnid': txnid,
            'productinfo': productinfo,
            'amount': amount,
            'email': email,
            'firstname': firstname,
            'surl': surl,
            'furl': furl,
            'phone': phone,
            'hash': hash_value
        }

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """ Override of payment to find the transaction based on Payu data.

        :param str provider_code: The code of the provider that handled the transaction
        :param dict notification_data: The notification data sent by the provider
        :return: The transaction if found
        :rtype: recordset of `payment.transaction`
        :raise: ValidationError if the data match no transaction
        """
        tx = super()._get_tx_from_notification_data(provider_code,
                                                    notification_data)
        if provider_code != 'payu' or len(tx) == 1:
            return tx

        reference = notification_data.get('productinfo')
        tx = self.search(
            [('reference', '=', reference), ('provider_code', '=', 'payu')]
        )
        if not tx:
            raise ValidationError("Payu: " + _(
                "No transaction found matching reference %s.", reference
            ))
        return tx

    def _process_notification_data(self, notification_data):
        """ Override of payment to process the transaction based on Payu data.

        Note: self.ensure_one()

        :param dict notification_data: The notification data sent by the provider
        :return: None
        """
        super()._process_notification_data(notification_data)
        if self.provider_code != 'payu':
            return

        # Update the provider reference.
        provider_reference = self._payu_prepare_payment_request_payload()
        self.provider_reference = provider_reference['txnid']

        # update payment state
        payment_status = notification_data.get('status')
        if payment_status == 'success':
            self._set_done()
        elif payment_status == 'failure':
            self._set_canceled("Payu: " + _("Cancelled payment with status: %s",
                                            payment_status))
        else:
            _logger.info(
                "received data with invalid payment status (%s) for transaction with reference %s",
                payment_status, self.reference
            )
            self._set_error(
                "Payu: " + _("Received data with invalid payment status: %s",
                             payment_status)
            )
