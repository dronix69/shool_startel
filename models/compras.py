# -*- coding: utf-8 -*-
from odoo import models, fields, api
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




