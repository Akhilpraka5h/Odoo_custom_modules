{
    'name': 'Automatic Sale Order',
    'version': '1.0',
    'summary': 'Automated Sale order with button click',
    'website': 'www.odoo.com',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_view.xml',
        'wizard/add_product_to_quotation.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
