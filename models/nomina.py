# -*- coding: utf-8 -*-

from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

from odoo.osv import expression

class NominaCert(models.Model):
    _name = 'cert.nomina'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Nomina Empleados'

    name = fields.Many2one('hr.employee', string='Empleados', required=True,)
    rut = fields.Char(string='Rut', related="name.identification_id")
    poste = fields.Char(related='name.job_title', string='Puesto de Trabajo')
    date = fields.Date('Fecha', default=fields.Date.today())
    sale = fields.Integer(string='Sueldo dias Trabajados', compute='_sale', help='Son los Dias que Trabajo el Empleado')
    bonus = fields.Integer(string='Bonificación Imponible')
    extra = fields.Integer(string='Horas Extras')
    gratuity = fields.Integer(string='Gratificación Legal', compute='_gratuity')
    afp = fields.Integer(string='AFP', compute='_afp', store=True)
    afp_id = fields.Float(string='Fondo AFP %', related='contract_id.afp_id')
    fonasa = fields.Integer(string='Fonasa / Isapre', compute='_fonasa', store=True)
    fonasa_id = fields.Float(string='Fonasa %', related='contract_id.fonasa_id')
    sure = fields.Integer(string='Seguro de Cesantia', compute='_sure')
    sure_id = fields.Float(string='Seguro %', related='contract_id.sure_id')
    tax = fields.Integer(string='Impuesto Unico')
    family = fields.Integer(string='Cargas Familiares')
    car = fields.Integer(string='Asignación Locomoción')
    lunch = fields.Integer(string='Asignación de Colación')

    taxi = fields.Integer(string='Haberes Imponibles', compute='_taxi')
    tax_id = fields.Integer(string='Haberes No Imponibles', compute='_tax_id')
    discount = fields.Integer(string='Descuentos', compute='_discount')
    pay = fields.Integer(string='Liquido a Pagar', compute='_pay', store=True)
    month = fields.Selection([('E', 'Enero'), ('F', 'Febrero'), ('M', 'Marzo'), ('A', 'Abril'), ('Z', 'Mayo'),
                              ('J', 'Junio'), ('X', 'Julio'), ('B', 'Agosto'), ('S', 'Septiembre'), ('O', 'Octubre'),
                              ('N', 'Noviembre'), ('D', 'Diciembre')], default=' ')

    contract_id = fields.Many2one('hr.contract', string='Contracto', required=True)
    days = fields.Integer(string='Dias Trabajados', required=True)
    sale_id = fields.Integer(string='Sueldo Base', related='contract_id.sale', store=True)


    @api.depends('days','sale_id')
    def _sale(self):
        for r in self:
            her = r.days
            jer = r.sale_id /30
            ger = jer * her
            if her <= 30:
                r.sale = ger
            else:
                r.sale = 0

    @api.depends('sale','bonus','extra')
    def _gratuity(self):
        for r in self:
            gratuity = 0.25*(r.sale+r.bonus+r.extra)
            if gratuity <= 158333:
                r.gratuity = gratuity
            else:
                r.gratuity = 158333

    @api.depends('sale','bonus','extra','gratuity')
    def _taxi(self):
        for r in self:
            r.taxi = r.sale+r.bonus+r.extra+r.gratuity

    @api.depends('family','car','lunch')
    def _tax_id(self):
        for r in self:
            r.tax_id = r.family+r.car+r.lunch

    @api.depends('taxi','sure_id')
    def _sure(self):
        for r in self:
            r.sure =  r.sure_id*r.taxi/100

    @api.depends('taxi','fonasa_id')
    def _fonasa(self):
        for r in self:
            r.fonasa = r.fonasa_id*r.taxi/100

    @api.depends('taxi','afp_id')
    def _afp(self):
       for r in self:
          r.afp = r.afp_id*r.taxi/100

    @api.depends('afp','fonasa','sure','tax')
    def _discount(self):
        for r in self:
            r.discount = r.afp+r.fonasa+r.sure+r.tax

    @api.depends('taxi','tax_id','discount')
    def _pay(self):
        for r in self:
            r.pay = r.taxi+r.tax_id-r.discount


