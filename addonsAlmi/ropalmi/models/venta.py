from odoo import models, fields, api

class Venta(models.Model):
    _name = 'venta'
    _description = 'Venta'

    name = fields.Char(string="Referencia", required=True, default="Nueva")
    fecha = fields.Date(string="Fecha", default=fields.Date.today)
    product_lines = fields.One2many('venta.line', 'venta_id', string="Productos")
    total = fields.Float(string="Subtotal", compute='_compute_total')
    iva = fields.Float(string="IVA (21%)", compute='_compute_iva')
    venta_total = fields.Float(string="Total con IVA", compute='_compute_venta_total')
    metodo_pago = fields.Selection([
        ('tarjeta', 'Tarjeta'),
        ('efectivo', 'Efectivo')
    ], string="Método de Pago", required=True)
    currency_id = fields.Many2one(
        'res.currency', string='Moneda', default=lambda self: self.env.company.currency_id)

    @api.depends('product_lines.subtotal')
    def _compute_total(self):
        for record in self:
            record.total = sum(line.subtotal for line in record.product_lines)

    @api.depends('total')
    def _compute_iva(self):
        for record in self:
            record.iva = record.total * 0.21

    @api.depends('total', 'iva')
    def _compute_venta_total(self):
        for record in self:
            record.venta_total = record.total + record.iva




class VentaLine(models.Model):
    _name = 'venta.line'
    _description = 'Venta Line'

    venta_id = fields.Many2one('venta', string="Venta", required=True)
    product_id = fields.Many2one('stock.item', string="Producto", required=True)
    talla_id = fields.Many2one('stock.size', string="Talla", domain="[('stock_item_id', '=', product_id)]", required=True)
    cantidad = fields.Integer(string="Cantidad", default=1)
    precio = fields.Float(string="Precio Unitario", related='product_id.precio')
    subtotal = fields.Float(string="Subtotal", compute='_compute_subtotal')

    @api.depends('cantidad', 'precio')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.cantidad * line.precio

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Actualizar las tallas disponibles cuando se selecciona un producto."""
        if self.product_id:
            return {'domain': {'talla_id': [('stock_item_id', '=', self.product_id.id)]}}
        else:
            return {'domain': {'talla_id': []}}

