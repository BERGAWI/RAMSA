# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': "Sales Custom",
    'version': "16.0.0.0",
    'author': "Debug",
    'description': ''' ''',
    'category': "Sales",
    'depends': ['sale', 'sale_management', 'stock', 'sale_stock',
                'product', 'purchase', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'security/product_groups.xml',

        'views/sales_representative_view.xml',
        'views/representative_company_view.xml',
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
        'views/stock_picking_views.xml',
        'views/stock_move.xml',
        'views/invoice_views.xml',
        'views/res_config_settings.xml',
        'reports/sale_print.xml',
        'reports/invoice_templates.xml',
        'reports/sale_templates.xml',
        'reports/purchase_templates.xml',
        'reports/picking_templates.xml',
        'reports/sale_representative_print.xml',
        'wizard/sale_wizard.xml',
    ],
    'auto_install': False,
}
