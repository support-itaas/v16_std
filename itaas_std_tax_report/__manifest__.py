# -*- coding: utf-8 -*-
# Part of ITAAS (www.itaas.co.th)

{
    'name': 'Itaas Std Tax Report',
    'version': '16.0.0.0',
    'price': 'Free',
    'currency': 'THB',
    'category': 'Itaas Std Tax Report',
    'summary': 'Itaas Std Tax Report',
    'author': 'IT as a Service Co., Ltd.',
    'website': 'www.itaas.co.th',
    'depends': ['base','account','itaas_partner_detail_address','itaas_company_detail_address'],
    'data': [
        #wizard
        'wizard/tax_report_view.xml',
        # views
        'views/account_tax_view.xml',
        'views/account_move_view.xml',
        'views/account_account_view.xml',
        # report

        #security
        'security/ir.model.access.csv',
    ],

    'qweb': [],
    "installable": True,
    "application": True,
    "auto_install": False,
}
