{
    'name': 'Sale Order Task',
    'version': '1.0',
    'summary': 'Add selection to sale order',
    'website': 'www.odoo.com',
    'depends': ['sale', 'stock'],
    'data': [
        'views/sale_order_view.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
