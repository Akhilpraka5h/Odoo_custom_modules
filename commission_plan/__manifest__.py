# -*- coding: utf-8 -*-
{
    'name': 'Commission Plan',
    'version': '1.0',
    'category': 'Custom',
    'summary': 'Commission plan for salesperson',
    'website': 'www.odoo.com',
    'depends': ['sale', 'mail'],
    'data': [
        'data/commission_plan_sequence.xml',
        'security/ir.model.access.csv',
        'views/crm_commission_view.xml',
        'views/commission_product_line_view.xml',
        'views/res_user_view.xml',
        'views/crm_team_view.xml',
        'views/commission_revenue_wise_view.xml',
        'views/commission_plan_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
