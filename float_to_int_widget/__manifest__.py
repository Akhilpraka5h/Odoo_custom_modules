# -*- coding: utf-8 -*-
{
    'name': 'Float Int',
    'version': '18.0.1.0.0',
    'category': 'Custom',
    'summary': 'Convert float value to nearest integer value',
    'website': 'www.odoo.com',
    'data': [
        'views/res_partner_views.xml',
    ],
    'assets':
        {
            'web.assets_backend':
                {
                    '/float_to_int_widget/static/src/xml/float_int.xml',
                    '/float_to_int_widget/static/src/js/float_int.js',
                },
        },
    'installable': True,
    'license': 'LGPL-3',
}
