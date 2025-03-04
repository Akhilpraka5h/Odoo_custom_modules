# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Payment Provider: PayU",
    'version': '1.0',
    'category': 'Accounting/Payment Providers',
    'sequence': 350,
    'summary': "A payment provider covering India.",
    'description': "Payu Payment Provider",
    'depends': ['payment'],
    'data': [
        'data/payment_provider_data.xml',
        'views/payment_provider_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
        ],
    },
    'license': 'LGPL-3',
}
