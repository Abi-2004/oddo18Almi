{
    'name': 'ROPALMI - Clothing Shop Management',
    'version': '1.0',
    'author': 'Your Name',
    'category': 'Sales',
    'depends': ['base', 'sale_management'],
    'data': [
        'views/menu.xml',
        'views/stock_views.xml',
        'views/venta_views.xml',
        'views/stock_item_kanban_view.xml',
        'views/venta_kanban_view.xml',
        'reports/report_venta.xml'  # Esto es crucial
    ],

    'installable': True,
    'auto_install': False,
}