from odoo import _, models
from werkzeug import urls
import urllib.parse
# from odoo.exceptions import ValidationError
from odoo.addons.payment_payu.controllers.main import PayuController
import hashlib


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'payu':
            return res
        payload = self._payu_prepare_payment_request_payload()
        api_url = 'https://test.payu.in/_payment'
        return {'api_url': api_url,
                'url_params': payload}

    def _payu_prepare_payment_request_payload(self):
        base_url = self.provider_id.get_base_url().replace("http://", "")
        print(self.provider_id.get_base_url())
        redirect_url = urls.url_join(base_url, PayuController._return_url)
        key = self.provider_id.payu_api_key
        txnid = self.reference
        productinfo = "Odoo Payment"
        amount = self.amount
        email = self.partner_email
        firstname = self.partner_name
        surl = redirect_url
        furl = base_url
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
