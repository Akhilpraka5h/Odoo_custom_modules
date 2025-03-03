-- disable paypal payment provider
UPDATE payment_provider
   SET payu_email_account = NULL,
       payu_client_id = NULL,
       payu_client_secret = NULL;
