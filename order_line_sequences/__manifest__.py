{
    'name': 'Order Line Sequences/Line Numbers',
    'version': '16.0.1.0.0',
    'depends': ['base', 'sale_management', 'purchase', 'stock','account'],
    'data': [
        'views/sale_order_view.xml',
        'views/purchase_order_view.xml',
        'views/stock_view.xml',
        'views/invoices_views.xml',
        'reports/sale_order_document_view.xml',
        'reports/report_picking_view.xml',
        'reports/report_purchaseorder_document_view.xml',
        'reports/report_invoice_view.xml',
    ],
}
