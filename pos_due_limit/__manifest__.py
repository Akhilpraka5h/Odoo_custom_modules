{
    'name': 'POS Due Limit',
    'version': '18.0.1.0.0',
    'summary': 'Due Limit for Customers',
    'website': 'www.odoo.com',
    'depends': ['account', 'point_of_sale'],
    'data': [
        'views/res_partner_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            '/pos_due_limit/static/src/js/payment_screen.js',
            '/pos_due_limit/static/src/xml/partner_line.xml',
            '/pos_due_limit/static/src/xml/partner_list.xml',
        ]
    },
    'installable': True,
    'license': 'LGPL-3',
}
