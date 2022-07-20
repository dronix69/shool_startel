# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, date
import logging
import re


class CertSimulador(models.Model):
    _name = 'cert.simulador'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Crea un registro para las practicas del simuldor'

    name = fields.Char(string='Nombre Alumno')
    practice = fields.Integer(string='Nº Practica', required=True)
    date = fields.Date('Fecha', default=fields.Date.today())
    code = fields.Many2one('cert.codigo', 'Codigo')
    palanca = fields.Selection([('A', 'Aprobado'), ('R', 'Rechazado')], string='Test de Palanca')
    simple = fields.Selection([('A', 'Aprobado'), ('R', 'Rechazado')], string='Test Reaccion Simple')
    punteo = fields.Selection([('A', 'Aprobado'), ('R', 'Rechazado')], string='Test Punteado')
    vision = fields.Selection([('A', 'Aprobado'), ('R', 'Rechazado')], string='Exa a la Vista')

    @api.onchange('code')
    def _onchange_code(self):
        for record in self:
            if record.code:
                record.name = record.code.name_last


class CertCodigo(models.Model):
    _name = 'cert.codigo'
    _description = 'Crear numero de codigo del Alumno'

    name = fields.Char(string='Numero del Codigo', required=True)
    name_last = fields.Char(string='Nombre', required=True)
    date_id = fields.Date('Fecha Creación', default=fields.Date.today())
    word = fields.Many2one('hr.employee', 'Responsable', required=True)
    student = fields.One2many('cert.simulador', 'code', 'Alumnos')
    student_count = fields.Integer(string="Total Simulación", compute="compute_student_count")

    def get_simulacion(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Practicas',
            'view_mode': 'tree',
            'res_model': 'cert.simulador',
            'domain': [('code', '=', self.id)],
            'context': "{'create': False}"
        }

    def compute_student_count(self):
        for record in self:
            record.student_count = self.env['cert.simulador'].search_count([('code', '=', self.id)])













