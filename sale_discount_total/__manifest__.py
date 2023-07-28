{
    'name': 'Sale Discount on Total Amount',
    'version': '16.0.1.1.0',
    'category': 'Sales Management',
    'depends': ['sale',
                'account', 'delivery'
                ],
    'data': [
        'views/res_config_view.xml',
        'views/sale_view.xml',
        'views/account_invoice_view.xml',
        'views/invoice_report.xml',
        'views/sale_order_report.xml',
        'reports/sale_templates.xml',
        'reports/invoice_templates.xml',
    ],
}