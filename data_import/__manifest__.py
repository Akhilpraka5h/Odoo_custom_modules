# -*- coding: utf-8 -*-
{
    'name': 'Data Import',
    'version': '1.0',
    'category': 'Custom',
    'summary': 'Import Data from excel',
    'website': 'www.odoo.com',
    'depends': ['stock'],
    'data': [
        'secuirty/ir.model.access.csv',
        'wizard/import_lot_serial_view.xml',
        'views/stock_lot_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'data_import/static/src/js/*.js',
            'data_import/static/src/xml/*.xml',

        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
