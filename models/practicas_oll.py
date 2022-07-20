# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, date, timedelta
import logging
import re


class CertPracticas(models.Model):
    _name = 'cert.practicas'
    _description = 'Crea un registro de las citas a practicas de conduccion'

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


    name = fields.Char(string='Nombre del Alumno')
    ward = fields.Many2one('cert.alumno', 'Rut')
    fhone = fields.Char(string='Telefono')
    lessons = fields.Char(string='Nº de Práctica', required=True)
    instructor = fields.Many2one('cert.instructor', 'Instructor', required=True)
    date_first = fields.Datetime(string='Fecha y Hora Inicio', required=True)
    date_last = fields.Datetime(string='Hora Termino')
    duration = fields.Float(string='Duración', compute='_compute_duration', help='Duración en Horas')


    @api.onchange('ward')
    def _onchange_ward(self):
        for record in self:
            if record.ward:
                record.name = record.ward.name_id




class CertAlumno(models.Model):
    _name = 'cert.alumno'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Crear registro de alumno para tomar hora de practicas'

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
    _descripcion = 'Registro de los instructores'


    name = fields.Char(string='Nombre', required=True )
    date = fields.Date(string='Fecha', required=True)
    card = fields.Char(string='Marca', required=True)
    model = fields.Char(string='Modelo', required=True)
    patente = fields.Char(string='Patente', required=True)