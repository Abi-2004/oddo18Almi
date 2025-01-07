# -*- coding: utf-8 -*-
# Part of Odoo. Modulo de peliculas realizado en ALMI
{
    'name': 'Modulo de Peliculas',
    'version': '1.0',
    'depends' : ['base','contacts','mail'],
    'author' : 'Almi',
    'category': 'Peliculas',
    'website': '',
    'description': 'Modulo para realizar presupuestos de peliculas',
    'data': [
        'views/menu.xml',
        'views/stock_views.xml',
        'views/venta_views.xml',
        'views/stock_item_kanban_view.xml',
        'views/venta_kanban_view.xml',
        'reports/venta_report_templates.xml',
        'reports/venta_report.xml'  # Esto es crucial
    ],
}