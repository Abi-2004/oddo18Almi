# -*- coding: utf-8 -*-

from odoo import fields, models, api

class UpdateWizard(models.TransientModel):
    _name = 'update.wizard'
    _description = ' '

    name = fields.Text(string = 'Nueva descripcion')

    def update_vista_general(self):
        presupuesto_obj = self.env['presupuesto']
        presupuesto_id = presupuesto_obj.browse(self._context['active_id'])
        presupuesto_id.vista_general = self.name