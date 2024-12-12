# -*- coding: utf-8 -*-
from odoo import fields, models

class Libro(models.Model):
    _name = 'libro'

    name = fields.Char(string='Nombre')
    autor = fields.Char(string='Autor')
    fecha_publicacion = fields.Date(string='Fecha de Publicacion')
    descripcion = fields.Text(string='Descripcion')
