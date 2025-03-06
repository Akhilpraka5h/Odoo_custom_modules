# -*- coding: utf-8 -*-

{
    'name': 'Payment Provider: payU',
    'version': '1.0',
    'category': 'Accounting/Payment Providers',
    'summary': "PayU is a global payment service provider offering online payment solutions in emerging markets",
    'description': " ",
    'website': 'https://payu.in',
    'depends': ['payment'],
    'data': [
        'views/payment_payu_templates.xml',
        'data/payment_provider_data.xml',
        'views/payment_provider_views.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'license': 'LGPL-3',

}
