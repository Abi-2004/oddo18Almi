# -*- coding: utf-8 -*-
from email.policy import default
import logging
from odoo import fields, models, api
logger = logging.getLogger(__name__)

class Presupuesto (models.Model):
    _name = 'presupuesto'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin']

    name = fields.Char(string='Pelicula')
    clasificacion = fields.Selection(selection = [
        ('G', 'G'),
        ('PG', 'PG'),
        ('PG-13', 'PG-13'),
        ('R', 'R'),
        ('NC-17', 'NC-17'),
        ], string='Clasificación')
    fecha_estreno = fields.Date(string ='Fecha de Estreno')
    vista_general = fields.Text(string ='Descripcion')
    libro_filename = fields.Char(string ='Nombre del libro')
    puntuacion = fields.Integer(string ='Puntuacion', related='puntuacion2')
    puntuacion2 = fields.Integer(string ='Puntuacion2')
    active = fields.Boolean(string ='Activo')
    director_id = fields.Many2one(comodel_name='res.partner',string='Director')
    categoria_director_id = fields.Many2one(comodel_name='res.partner.category',
                                            string='Categoria director',
                                            default=lambda self: self.env['res.partner.category'].search([('name', '=', 'Director')]))
    generos_id = fields.Many2many(comodel_name='genero',string='Generos')
    descripcion = fields.Text(string='Descripcion')
    link_trailer = fields.Char(string='Trailer')
    es_libro = fields.Boolean(string='Version libro')
    libro = fields.Binary(string='Libro')
    state = fields.Selection(selection=[
        ('borrador', 'Borrador'),
        ('aprobado', 'Aprobado'),
        ('cancelado', 'Cancelado'),
        ], default='borrador', string='Estado', copy=False)

    fch_aprobado = fields.Datetime(string='Fecha aprobado', copy=False)

    def aprobar_presupuesto(self):
        self.state = 'aprobado'
        self.fch_aprobado = fields.Datetime.now()
        logger.info("**********Presupuesto aprobado**********")

    def cancelar_presupuesto(self):
        self.state = 'cancelado'
        logger.info("**********Presupuesto cancelado**********")