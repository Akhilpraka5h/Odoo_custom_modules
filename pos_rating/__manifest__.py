{
    'name': 'POS Product Rating',
    'version': '18.0.1.0.0',
    'summary': 'Rating the product Quality',
    'website': 'www.odoo.com',
    'depends': ['point_of_sale'],
    'data': [
        'view/product_product_view.xml'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            '/pos_rating/static/src/js/product_card.js',
            '/pos_rating/static/src/js/pos_order_line.js',
            '/pos_rating/static/src/xml/pos_product_card.xml',
            '/pos_rating/static/src/xml/pos_product_order_line.xml',
            '/pos_rating/static/src/xml/pos_rating_template.xml',
        ]
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
