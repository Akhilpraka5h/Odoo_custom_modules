{
    'name': 'POS Product Rating',
    'version': '1.0',
    'summary': 'Rating the product Quality',
    'website': 'www.odoo.com',
    'depends': ['product', 'point_of_sale'],
    'data': [
        'view/product_product_view.xml'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            '/pos_rating/static/xml/product_card.xml',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
