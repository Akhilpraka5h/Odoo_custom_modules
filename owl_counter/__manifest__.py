# -*- coding: utf-8 -*-
{
    'name': 'Counter',
    'version': '18.0.1.0.0',
    'category': 'Custom',
    'summary': 'Counter App On Owl',
    'website': 'www.odoo.com',
    'data': [
        'views/counter.xml',
    ],
    'assets':
        {
            'web.assets_backend':
                {
                    '/owl_counter/static/src/js/counter.js',
                    '/owl_counter/static/src/js/reset.js',
                    '/owl_counter/static/src/xml/counter.xml',
                },
        },
    'installable': True,
    'license': 'LGPL-3',
}
