# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, date, timedelta
import logging
import re
import time

class CursCert(models.Model):
    _name = 'cert.cursos'
    _description = 'Registro Cursos'

    secuencia = fields.Integer(string='Total Alumno')
    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    codigo = fields.Char(string='Codigo Curso', required=True)
    number = fields.Selection([('BO', 'BO'), ('BP', 'BP'), ('A2', 'A2'), ('A3', 'A3'), ('A4', 'A4'), ('A5', 'A5'),
                               ('A2-A4', 'A2-A4'), ('A3-A5', 'A3-A5')], default='Select')
    date = fields.Date(string='Fecha Creacion')
    fridname = fields.Many2one('hr.employee', 'Empleado', required=True)
    student = fields.One2many('res.partner', 'student', 'Alumnos')
    modal_id = fields.Selection(
        [('P', 'Presencial'), ('O', 'Online')], string='Modalidad')


#Modelo que crea un numero de secuencia en tu formulario.
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('cert.cursos') or _('New')
        res = super(CursCert, self).create(vals)
        return res



class ImagenPdf(models.Model):
    _name = 'imagen.pdf'

    name = fields.Char(string='Titulo', required=True)
    img = fields.Binary(string='Imagen')


class CertAsignatura(models.Model):
    _name = 'cert.asignatura'
    _description = 'Asignatura'

    name = fields.Char(string='Nombre Asignatura', required=True)
    date_start = fields.Date(string='Fecha de Creación')
    color = fields.Integer(string='color')


class CertClases(models.Model):
    _name = 'cert.clases'
    _description = 'Registro Clases'

    @api.depends("date_start", "date_stop")
    def _compute_duration(self):
        duration = 0.0
        for rec in self:
            if rec.date_start and rec.date_stop:
                start = fields.Datetime.from_string(rec.date_start)
                end = fields.Datetime.from_string(rec.date_stop)
                delta = end - start
                duration = delta.total_seconds() / 3600
            rec.duration = duration

    def action_confirm(self):
        for rec in self:
            rec.state = 'A'

    def action_done(self):
        for rec in self:
            rec.state = 'B'

    name = fields.Many2one('cert.instructor', 'Profesor', required=True)
    date_start = fields.Datetime(string='Fecha Inicio')
    date_stop = fields.Datetime(string='Fecha Termino')
    duration = fields.Float(string='Duración', compute='_compute_duration', help='Duración en Horas')
    course = fields.Many2many('cert.asignatura', string="Asignaturas")
    comment = fields.Text('Comentarios', help='Comentarios')
    state = fields.Selection([('A', 'Clase no Realizada'), ('B', 'Completado')], default='A')
    course_id = fields.Selection([('BO', 'BO'), ('BP', 'BP'), ('A2', 'A2'), ('A3', 'A3'), ('A4', 'A4'), ('A5', 'A5'),
                               ('A2-A4', 'A2-A4'), ('A3-A5', 'A3-A5')], default='Select', string='Curso')
    jornada = fields.Selection(
        [('M', 'Mañana'), ('T', 'Tarde'), ('V', 'Vespertino')], string='Jornada')



