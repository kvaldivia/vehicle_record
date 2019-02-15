# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError

from datetime import datetime, date, timedelta
from dateutil.parser import parse

VEHICLE_STATUS_CHECKED = 'checked'
VEHICLE_STATUS_PENDING = 'pending'
VEHICLE_STATUS_UNCHECKED = 'unchecked'
VEHICLE_STATUS = [
    (VEHICLE_STATUS_CHECKED, 'Revisado'),
    (VEHICLE_STATUS_PENDING, 'Revision pendiente'),
    (VEHICLE_STATUS_UNCHECKED, 'Revision omitida'),
]


class Vehicle(models.Model):
    _name = 'vehicle_record.vehicle'
    plate_number = fields.Char('Numero de placa', required=True)
    brand_name = fields.Char('Nombre de marca')
    model_name = fields.Char('Nombre de modelo')
    mileage = fields.Float('Kilometraje', store=True)
    status = fields.Selection(
        VEHICLE_STATUS, string='Estado', default='unchecked'
    )
    current_status = fields.Char('Estado actual', default='unchecked')
    next_maintenance = fields.Date('Siguiente mantenimiento')
    maintenance_record = fields.One2many(
        comodel_name='vehicle_record.vehicle.maintenance.record',
        inverse_name='vehicle',
        string='Registro de mantenimiento'
    )

    @api.model
    def create(self, data):
        if 'maintenance_record' not in data.keys():
            raise UserError(
                'Debe programar al menos un mantenimiento para el vehiculo')
        import pudb; pudb.set_trace()
        values = data['maintenance_record']
        data['status'] = self.update_status(values=values)
        data['current_status'] = data['status']
        return super(Vehicle, self).create(data)

    def update_status(self, values=None, records=None):
        today = datetime.now()
        date_diff = None
        if values:
            date_diff = self._date_diff_from_values(values)
        elif records:
            date_diff = self._date_diff_from_records(records)
        else:
            date_diff = self._date_diff_from_records(self.maintenance_record)

        if date_diff < 0:
            return VEHICLE_STATUS_UNCHECKED
        elif date_diff <= 15:
            return VEHICLE_STATUS_PENDING
        else:
            return VEHICLE_STATUS_CHECKED

        return result

    def _date_diff_from_values(self, values, time=datetime.now()):
        if len(values) == 0:
            return
        maintenance_row = values[0]
        maintenance = maintenance_row[2]
        if maintenance['status'] in 'scheduled':
            diff = self._date_diff_in_days(maintenance['due_date'], time)
            if diff < 0:
                maintenance['status'] = 'missed'
            return diff
        return 1

    def _date_diff_from_records(self, records, time=datetime.now()):
        if len(records) == 0:
            return
        maintenance = records[0]
        if maintenance.status in 'scheduled':
            diff = self._date_diff_in_days(maintenance.due_date, time)
            if diff < 0:
                maintenance.status = 'missed'
            return diff
        return 1
            
    def _date_diff_in_days(self, date_a, date_b):
        diff = parse(date_a).date() - date_b.date()
        return diff.days


    @api.depends('maintenance_record')
    def on_maintenance_record_changed(self):
        self._update_status()

    @api.model
    def cron_update_status(self):
        self._update_status()

    @api.one
    @api.depends('status')
    def update_current_status_key(self):
        for state in VEHICLE_STATUS:
            import pudb
            pudb.set_trace()
            key = state[0]
            value = state[1]
            if self.status == value:
                self.current_status = key
                return


class VehicleMaintenance(models.Model):
    _name = 'vehicle_record.vehicle.maintenance.record'
    _order = 'due_date, date_created desc'
    date_created = fields.Datetime(default=datetime.now())
    due_date = fields.Datetime('Fecha programada', required=True)
    started = fields.Datetime('Fecha inicio')
    finished = fields.Datetime('Fecha fin')
    next_maintenance_date = fields.Datetime('Fecha de siguiente mantenimiento')
    description = fields.Text('Detalle del mantenimiento')
    status = fields.Selection([
        ('draft', 'borrador'),
        ('missed', 'no realizado'),
        ('scheduled', 'programado'),
        ('inprogress', 'en progreso'),
        ('finished', 'realizado'),
    ], 'Estado', default='draft')
    vehicle = fields.Many2one(
        comodel_name='vehicle_record.vehicle',
        string='Vehiculo',
        on_delete='restrict'
    )

    @api.multi
    def execute_maintenance(self):
        status = 'inprogress'
        started = datetime.now()
        self.write({'status': status, 'started': started})
        self.vehicle.write({'status': self.vehicle.update_status()})

    @api.multi
    def finish_maintenance(self):
        status = 'finished'
        finished = datetime.now()
        if not self.next_maintenance_date:
            raise UserError('Debe indicar cuando se realizara el siguiente mantenimiento')
        self.write({
            'status': status,
            'finished': finished,
            'next_maintenance_date': self.next_maintenance_date
        })
        self.vehicle.write({'status': self.vehicle.update_status()})

    @api.model
    def create(self, data):
        data['status'] = 'scheduled'
        return super(VehicleMaintenance, self).create(data)
