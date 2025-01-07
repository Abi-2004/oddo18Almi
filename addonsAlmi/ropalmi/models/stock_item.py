from odoo import models, fields, api


class StockItem(models.Model):
    _name = 'stock.item'
    _description = 'Stock Item'

    name = fields.Char(string="Nombre", required=True)
    marca = fields.Char(string="Marca")
    color = fields.Char(string="Color")
    size_stock_ids = fields.One2many('stock.size', 'stock_item_id', string="Tallas y Cantidades")
    precio = fields.Float(string="Precio", required=True)
    image = fields.Image(string="Imagen del Producto")

    size_summary = fields.Char(string="Tallas y Cantidades", compute="_compute_size_summary")

    @api.depends('size_stock_ids', 'size_stock_ids.size', 'size_stock_ids.cantidad')
    def _compute_size_summary(self):
        # Obtener la selección del campo size desde el modelo stock.size
        size_selection = self.env['stock.size']._fields['size'].selection
        selection_dict = dict(size_selection)

        for record in self:
            summary_lines = []
            for line in record.size_stock_ids:
                # Obtener la etiqueta legible para la talla
                size_display = selection_dict.get(line.size, line.size)
                summary_lines.append(f"{size_display}: {line.cantidad}")
            record.size_summary = ", ".join(summary_lines)


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
