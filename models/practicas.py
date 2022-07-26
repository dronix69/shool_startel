# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, date, timedelta
import logging
import re


class CertPracticas(models.Model):
    _name = 'cert.practicas'
    _description = 'Registro Practicas'

    @api.depends("date_first", "date_last")
    def _compute_duration(self):
        duration = 0.0
        for rec in self:
            if rec.date_first and rec.date_last:
                start = fields.Datetime.from_string(rec.date_first)
                end = fields.Datetime.from_string(rec.date_last)
                delta = end - start
                duration = delta.total_seconds() / 3600
            rec.duration = duration

    def action_confirm(self):
        for rec in self:
            rec.state = 'A'

    def action_done(self):
        for rec in self:
            rec.state = 'B'


    name = fields.Char(string='Nombre del Alumno')
    ward = fields.Many2one('cert.alumno', 'Rut')
    fhone = fields.Char(string='Telefono')
    lessons = fields.Char(string='Nº de Práctica', required=True)
    instructor = fields.Many2one('cert.instructor', 'Instructor', required=True)
    date_first = fields.Datetime(string='Fecha y Hora Inicio', required=True)
    date_last = fields.Datetime(string='Hora Termino')
    duration = fields.Float(string='Duración', compute='_compute_duration', help='Duración en Horas')
    tick1 = fields.Boolean(string='Preconduccion')
    tick2 = fields.Boolean(string='Cambios de Pista y Virajes')
    tick3 = fields.Boolean(string='Ingreso a Circulación')
    tick4 = fields.Boolean(string='Detenciones y Estacionamiento')
    tick5 = fields.Boolean(string='Arranque, Aceleración y Frenado')
    tick6 = fields.Boolean(string='Transito Intenso')
    tick7 = fields.Boolean(string='Transito Moderado')
    km1 = fields.Integer(string='KM-Inicio')
    km2 = fields.Integer(string='KM-Final')
    total_id = fields.Integer(string='Total KM', compute='_total_id')
    comment = fields.Text('Comentarios', help='Comentarios')
    state = fields.Selection([('A', 'Sin Practica'), ('B', 'Completado')], default='A')
    digital_signatures = fields.Binary(string="Signatures")


    @api.onchange('ward')
    def _onchange_ward(self):
        for record in self:
            if record.ward:
                record.name = record.ward.name_id

    @api.depends('km1','km2')
    def _total_id(self):
        for r in self:
            r.total_id = r.km2-r.km1



class CertAlumno(models.Model):
    _name = 'cert.alumno'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Registro Alumno'

    reference = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    name = fields.Char(string='Rut', required=True)
    name_id = fields.Char(string='Nombre Alumno', required=True )
    date = fields.Date('Fecha')
    clase_id = fields.Integer(string='Total Prácticas')
    employee_ids = fields.Many2one('cert.instructor', 'Instructor')
    student = fields.One2many('cert.practicas', 'ward', 'Alumnos')
    image = fields.Binary(string='Imagen')
    student_count = fields.Integer(string="Total Practicas", compute="compute_student_count")

    def get_practicas(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name' : 'Practicas',
            'view_mode' : 'tree',
            'res_model' : 'cert.practicas',
            'domain' : [('ward', '=', self.id)],
            'context' : "{'create': False}"
        }
    def compute_student_count(self):
        for record in self:
            record.student_count  =self.env['cert.practicas'].search_count([('ward', '=', self.id)])

    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('cert.alumno') or _('New')
        res = super(CertAlumno, self).create(vals)
        return res





class CertInstructor(models.Model):
    _name = 'cert.instructor'
    _descripcion = 'Registro Instructores'


    name = fields.Char(string='Nombre', required=True )
    date = fields.Date(string='Fecha', required=True)
    card = fields.Many2one('fleet.vehicle.model.brand', required=True)
    model = fields.Char(string='Modelo', required=True)
    patente = fields.Char(string='Patente', required=True)