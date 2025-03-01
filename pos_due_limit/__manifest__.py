{
    'name': 'POS Due Limit',
    'version': '18.0.1.0.0',
    'summary': 'Due Limit for Customers',
    'website': 'www.odoo.com',
    'depends': ['account', 'point_of_sale'],
    'data': [
        'view/res_partner_view.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            '/pos_due_limit/static/src/js/payment_screen.js',
            '/pos_due_limit/static/src/xml/partner_line.xml',
        ]
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
