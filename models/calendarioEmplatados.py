from odoo import models, fields, api
import datetime

class CalendarioEmplatados(models.Model):
    _name = 'calendario.emplatados'
    _description = 'Calendario Emplatados'
    
    name = fields.Char(string='Name', required=True)
    selected_dates = fields.Many2many('calendar.event', string='Fechas Seleccionadas')
    day_set = fields.Selection([
        ('lunes_viernes', 'Lunes a Viernes'),
        ('miercoles_jueves', 'Miércoles y Jueves'),
        ('personalizado', 'Personalizado')
    ], string='Set de Días', default='personalizado')
    holidays = fields.One2many('calendario.emplatados.holiday', 'calendario_id', string='Festivos')

    NATIONAL_HOLIDAYS = [
        datetime.date(2024, 10, 12),  # 12 de octubre
        datetime.date(2024, 11, 1),   # 1 de noviembre
        datetime.date(2024, 12, 6),   # 6 de diciembre
        datetime.date(2024, 12, 9),   # 9 de diciembre
        datetime.date(2024, 2, 27),   # 27 de febrero
        datetime.date(2024, 2, 28),   # 28 de febrero
        datetime.date(2024, 4, 1),    # 1 de abril
        datetime.date(2024, 5, 1),    # 1 de mayo
    ]

    @api.onchange('day_set')
    def _onchange_day_set(self):
        if self.day_set == 'lunes_viernes':
            self._generate_events_for_lunes_a_viernes()
        elif self.day_set == 'miercoles_jueves':
            self._generate_events_for_miercoles_jueves()

    def _generate_events_for_lunes_a_viernes(self):
        today = datetime.date.today()
        events = []
        for i in range(30):  # Genera fechas para los próximos 30 días
            date = today + datetime.timedelta(days=i)
            if date.weekday() < 5:  # 0 = lunes, 1 = martes, ..., 4 = viernes
                event = self.env['calendar.event'].create({
                    'name': 'Fecha Seleccionada',
                    'start': datetime.datetime.combine(date, datetime.time.min),
                    'stop': datetime.datetime.combine(date, datetime.time.max)
                })
                events.append(event.id)
        self.selected_dates = [(6, 0, events)]

    def _generate_events_for_miercoles_jueves(self):
        today = datetime.date.today()
        events = []
        for i in range(30):  # Genera fechas para los próximos 30 días
            date = today + datetime.timedelta(days=i)
            if date.weekday() in (2, 3):  # 2 = miércoles, 3 = jueves
                event = self.env['calendar.event'].create({
                    'name': 'Fecha Seleccionada',
                    'start': datetime.datetime.combine(date, datetime.time.min),
                    'stop': datetime.datetime.combine(date, datetime.time.max)
                })
                events.append(event.id)
        self.selected_dates = [(6, 0, events)]

    @api.model
    def get_holidays_and_day_set(self, record_id):
        record = self.browse(record_id)
        holidays = record.holidays.mapped('date') + self.NATIONAL_HOLIDAYS
        day_set = record.day_set
        selected_dates = record.selected_dates.mapped('start') if record.selected_dates else []
        return {
            'holidays': holidays,
            'day_set': day_set,
            'selected_dates': selected_dates
        }

    @api.model
    def save_selected_date(self, record_id, date):
        record = self.browse(record_id)
        if not record.exists():
            return {'success': False, 'error': 'Record not found'}

        try:
            event = self.env['calendar.event'].create({
                'name': 'Fecha Seleccionada',
                'start': datetime.datetime.combine(date, datetime.time.min),
                'stop': datetime.datetime.combine(date, datetime.time.max)
            })
            record.write({'selected_dates': [(4, event.id)]})
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    @api.model
    def remove_selected_date(self, record_id, date):
        record = self.browse(record_id)
        if not record.exists():
            return {'success': False, 'error': 'Record not found'}

        try:
            event = self.env['calendar.event'].search([
                ('start', '=', datetime.datetime.combine(date, datetime.time.min)),
                ('id', 'in', record.selected_dates.ids)
            ], limit=1)
            if event:
                record.write({'selected_dates': [(3, event.id)]})
                event.unlink()
                return {'success': True}
            return {'success': False, 'error': 'Event not found'}
        except Exception as e:
            return {'success': False, 'error': str(e)}


class CalendarioEmplatadosHoliday(models.Model):
    _name = 'calendario.emplatados.holiday'
    _description = 'Festivos del Calendario Emplatados'

    calendario_id = fields.Many2one('calendario.emplatados', string='Calendario')
    date = fields.Date(string='Fecha', required=True)
