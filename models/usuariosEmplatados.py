# -*- coding: utf-8 -*-
# models/usuariosEmplatados.py

from odoo import models, fields, api

class UsuariosEmplatados(models.Model):
    _inherit = 'res.users'
    
    selected_dates = fields.Many2many('calendario.emplatados', string="Fechas Seleccionadas")
    
    @api.model
    def fetch_user_events(self, user_id):
        user = self.env['res.users'].browse(user_id)
        selected_dates = user.selected_dates.mapped('fecha')
        events = []
        for date in selected_dates:
            events.append({
                'title': 'Evento',
                'start': date,
                'allDay': True,
            })
        return events



    