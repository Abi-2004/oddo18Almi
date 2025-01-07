from odoo import models, fields, api


class Venta(models.Model):
    _name = 'venta'
    _description = 'Venta'

    name = fields.Char(string="Referencia", required=True, default="Nueva")
    fecha = fields.Date(string="Fecha", default=fields.Date.today)
    product_lines = fields.One2many('venta.line', 'venta_id', string="Productos")
    total = fields.Float(string="Total", compute='_compute_total')
    metodo_pago = fields.Selection([
        ('tarjeta', 'Tarjeta'),
        ('efectivo', 'Efectivo')
    ], string="Método de Pago", required=True)

    @api.depends('product_lines.subtotal')
    def _compute_total(self):
        for record in self:
            record.total = sum(line.subtotal for line in record.product_lines)

class VentaLine(models.Model):
    _name = 'venta.line'
    _description = 'Venta Line'

    venta_id = fields.Many2one('venta', string="Venta", required=True)
    product_id = fields.Many2one('stock.item', string="Producto", required=True)
    cantidad = fields.Integer(string="Cantidad", default=1)
    precio = fields.Float(string="Precio Unitario", related='product_id.precio')
    subtotal = fields.Float(string="Subtotal", compute='_compute_subtotal')

    @api.depends('cantidad', 'precio')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.cantidad * line.precio