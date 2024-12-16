# -*- coding: utf-8 -*-
from email.policy import default
import logging
from odoo import fields, models, api
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)

class Presupuesto (models.Model):
    _name = 'presupuesto'
    _inherit = ['mail.thread','mail.activity.mixin','image.mixin']

    name = fields.Char(string='Pelicula')
    clasificacion = fields.Selection(selection = [
        ('G', 'G'),  #Publico General
        ('PG','PG'), # Compañia de adulto
        ('PG-13','PG-13'), # Mayores de 13
        ('R','R'), #Compañia de adulto obligatorio
        ('NC-17','NC-17'), # Mayores de 18
    ], string='Clasificacion')
    dsc_clasificacion = fields.Char(string='Descripcion de la clasificacion')
    fecha_estreno = fields.Date(string='Fecha de estreno')
    vista_general = fields.Text(string='Description')
    libro_filename = fields.Char(string='Nombre del libro')
    puntuacion = fields.Integer(string='Puntuacion', related='puntuacion2')
    puntuacion2 = fields.Integer(string='Puntuacion2')
    active = fields.Boolean(string='Activo')
    director_id = fields.Many2one(comodel_name='res.partner',string='Director')
    actor_ids = fields.Many2many(comodel_name='res.partner',string='Actores')
    categoria_director_id = fields.Many2one(comodel_name='res.partner.category',
                                            string='Categoria director',
                                            # default= lambda self: self.env['res.partner.category'].search([('name', '=', 'Director')]))
                                            default=lambda self: self.env.ref('peliculas.category_director'))
    categoria_actor_id = fields.Many2one(comodel_name='res.partner.category',
                                            string='Categoria actor',
                                            # default= lambda self: self.env['res.partner.category'].search([('name', '=', 'Director')]))
                                            default=lambda self: self.env.ref('peliculas.category_actor'))
    opinion = fields.Html(string='opinion')
    generos_id = fields.Many2many(comodel_name='genero',string='Generos')
    descripcion = fields.Text(string='Descripcion')
    link_trailer = fields.Char(string='Trailer')
    es_libro = fields.Boolean(string='Versión Libro')
    libro = fields.Binary(string='Libro')
    state = fields.Selection(selection = [
        ('borrador', 'Borrador'),
        ('aprobado', 'Aprobado'),
        ('cancelado', 'Cancelado')
    ], default='borrador', string='Estado', copy=False)

    fch_aprobado = fields.Datetime(string='Fecha aprobado', copy = False)
    num_presupuesto = fields.Char(string='Numero de presupuesto', copy=False)
    detalle_ids = fields.One2many(
        comodel_name='presupuesto.detalle',
        inverse_name='presupuesto_id',
        string='detalles'
    )
    fecha_creacion = fields.Datetime(string='Fecha creacion', copy=False,
                                     default=lambda self:fields.Datetime.now())

    currency_id = fields.Many2one(comodel_name='res.currency', string = 'Moneda', default = lambda self: self.env.company.currency_id.id)
    terminos = fields.Text(string = 'Términos')
    base = fields.Monetary(string='Base Imponible', compute='_compute_total')
    impuestos = fields.Monetary(string='Impuestos', compute='_compute_total')
    total = fields.Monetary(string='Total', compute='_compute_total')

    @api.depends('detalle_ids')
    def _compute_total(self):
        for record in self:
            sub_total = 0
            for linea in record.detalle_ids:
                sub_total += linea.importe
            record.base = sub_total;
            record.impuestos = sub_total * 0.21
            record.total = sub_total * 1.21

    def aprobar_presupuesto(self):
        self.state = 'aprobado'
        self.fch_aprobado = fields.Datetime.now()
        logger.info('**************Presupuesto aprobado*******************************')

    def cancelar_presupuesto(self):
        self.state = 'cancelado'
        logger.info('******************Presupuesto cancelado********************************************')

    def unlink(self):
        logger.warning('******Eliminando presupuesto******')
        for presupuesto in self:
            if presupuesto.state == 'cancelado':
                super(Presupuesto, presupuesto).unlink()
            else:
                raise UserError('***No se puede eliminar***')
                #logger.error('***No se puede eliminar***')
    @api.model
    def create(self, variables):
        logger.info('***Create: {0}'.format(variables))
        sequence_obj = self.env['ir.sequence']
        siguiente_codigo = sequence_obj.next_by_code('secuencia.presupuesto.pelicula')
        variables['num_presupuesto']=siguiente_codigo
        logger.info('***Create: {0}'.format(siguiente_codigo))
        logger.info('***Create: {0}'.format(variables))
        return super(Presupuesto, self).create(variables)

    def write(self, variables):
        logger.info('***Edit: {0}'.format(variables))
        if 'clasificacion' in variables:
            raise UserError('***La clasificacion no se puede editar***')
        return super(Presupuesto, self).write(variables)

    def copy(self, default=None):
        default=dict(default or {})
        default['name']=self.name + " (copia)"
        return super(Presupuesto, self).copy(default)

    @api.onchange('clasificacion')
    def _onchange_clasificacion(self):
        if self.clasificacion:
            if self.clasificacion == 'G':
                self.dsc_clasificacion='Publico General'
            elif self.clasificacion == 'PG':
                self.dsc_clasificacion='Se recomienda la compañia de un adulto'
            elif self.clasificacion == 'PG-13':
                self.dsc_clasificacion='Mayores de 13'
            elif self.clasificacion == 'R':
                self.dsc_clasificacion='En compañia de un adulto'
            elif self.clasificacion == 'NC-17':
                self.dsc_clasificacion='Mayores de 18'
        else:
            self.dsc_clasificacion=False


class PresupuestoDetalle(models.Model):
    _name = 'presupuesto.detalle'

    presupuesto_id = fields.Many2one(comodel_name='presupuesto', string='Presupuesto')
    name = fields.Many2one(comodel_name='recurso.cinematografico', string='Recurso')
    description = fields.Char(string='Descripcion', related = 'name.descripcion')
    contacto_id = fields.Many2one(comodel_name='res.partner', string='Contacto', related='name.contacto_id')
    imagen = fields.Binary(string ='Imagen', related='name.imagen')
    cantidad = fields.Float(string = 'Cantidad', default='1.0')
    precio = fields.Float(string = 'Precio')
    importe = fields.Monetary(string = 'Importe')
    currency_id = fields.Many2one(comodel_name='res.currency', string='Moneda',
                                  default = lambda self: self.env.company.currency_id.id)

    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            self.importe = self.cantidad * self.precio

    @api.onchange('cantidad', 'precio')
    def _onchange_precio(self):
        self.importe = self.cantidad * self.precio
