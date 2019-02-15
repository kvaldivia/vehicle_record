# -*- coding: utf-8 -*-
from odoo import http

class VehicleRecord(http.Controller):
    @http.route('/vehicle_record/vehicle_record/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/vehicle_record/vehicle_record/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('vehicle_record.listing', {
            'root': '/vehicle_record/vehicle_record',
            'objects': http.request.env['vehicle_record.vehicle_record'].search([]),
            })

    @http.route('/vehicle_record/vehicle_record/objects/<model("vehicle_record.vehicle_record"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('vehicle_record.object', {
            'object': obj
            })
