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
    'data':[
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/update_wizard_views.xml',
        'report/reporte_pelicula.xml',
        'data/categoria.xml',
        'data/secuencia.xml',
        'views/menu.xml',
        'views/presupuesto_views.xml',
    ],
}