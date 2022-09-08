# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime, date, timedelta
import logging
import re


class CertCompras(models.Model):
    _name = 'cert.compras'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Modulo Compras'


    name = fields.Char(string='Boleta', required=True)
    date_id = fields.Datetime(string='Fecha', required=True)
    rut_id = fields.Char(string='Rut Empresa')
    coste = fields.Integer(string='Valor')
    clerk = fields.Many2one('hr.employee', 'Trabajador', required=True)
    metodo = fields.Selection([('E', 'Efectivo'), ('D', 'Debito'), ('C','Credito'), ('T','Transferencia')], string='Divisa')
    business = fields.Char(string='Nombre Empresa')
    type = fields.Selection([('B', 'Boleta'), ('F', 'Factura'), ('O','Otro')], string='Tipo Documento', default='B')
    description = fields.Text('Comentarios', help='Comentarios')



class CertGasoil(models.Model):
    _name = 'cert.gasoil'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Modulo Gasolina'

    #secuencia = fields.Integer(string='Total Alumno')
    name = fields.Char(string='Nº Reference', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    name_id = fields.Many2one('cert.instructor', 'Responzable', required=True)
    digito = fields.Char(string='Placa Patente', required=True)
    km = fields.Char(string='KM del Vehiculo', required=True)
    litro = fields.Integer(string='Litros de Combustible', required=True)
    gasoil_a = fields.Boolean('Octanos 93')
    gasoil_b = fields.Boolean('Octanos 95')
    gasoil_c = fields.Boolean('Octanos 97')
    gasoil_d = fields.Boolean('Diesel')
    voucher = fields.Char(string='Nº del Recibo', required=True)
    date = fields.Datetime(string='Fecha', default=fields.Date.today())

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('cert.gasoil') or _('New')
        res = super(CertGasoil, self).create(vals)
        return res

