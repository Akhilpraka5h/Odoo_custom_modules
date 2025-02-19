{
    'name': 'Add To Cart',
    'version': '1.0',
    'summary': 'Cart',
    'website': 'www.odoo.com',
    'depends': ['base', 'website', 'website_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/add_cart_view.xml'
    ],
    'installable': True,
    'license': 'LGPL-3',
}
