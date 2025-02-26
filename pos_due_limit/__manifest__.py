{
    'name': 'POS Due Limit',
    'version': '18.0.1.0.0',
    'summary': 'Due Limit for Customers',
    'website': 'www.odoo.com',
    'depends': ['point_of_sale'],
    'data': [
        'view/res_partner_view.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
        ]
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
