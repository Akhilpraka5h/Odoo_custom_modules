{
    'name': 'Recent View Product',
    'version': '1.0',
    'category': 'Custom',
    'summary': 'Cart',
    'website': 'www.odoo.com',
    'depends': ['website_sale'],
    'data': [
        'views/website_snippet.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/recent_view_product/static/src/js/recent_dynamic_snippet.js',
            '/recent_view_product/static/src/xml/recent_view_snippet_template.xml',
        ],
    },
    'installable': True,
    'license': 'LGPL-3',
}
