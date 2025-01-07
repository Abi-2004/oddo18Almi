from odoo import models, fields

class StockItem(models.Model):
    _name = 'stock.item'
    _description = 'Stock Item'

    name = fields.Char(string="Nombre", required=True)
    marca = fields.Char(string="Marca")
    color = fields.Char(string="Color")
    size_stock_ids = fields.One2many('stock.size', 'stock_item_id', string="Tallas y Cantidades")
    precio = fields.Float(string="Precio", required=True)
    image = fields.Image(string="Imagen del Producto")  # Add this line



class StockSize(models.Model):
    _name = 'stock.size'
    _description = 'Stock Size'

    stock_item_id = fields.Many2one('stock.item', string="Producto", required=True)
    size = fields.Selection([
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
    ], string="Talla", required=True)
    cantidad = fields.Integer(string="Cantidad", default=0)