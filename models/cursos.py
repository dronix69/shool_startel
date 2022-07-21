# -*- coding: utf-8 -*-

from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

from odoo.osv import expression


class CursCert(models.Model):
    _name = 'cert.cursos'
    _description = 'Crear registro de los cursos'

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


class NominaCert(models.Model):
    _name = 'cert.nomina'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Modulo para llevar un control de los pagos a los Empleados'

    name = fields.Many2one('hr.employee', string='Empleados', required=True,)
    rut = fields.Char(string='Rut', related="name.identification_id")
    poste = fields.Char(related='name.job_title', string='Puesto de Trabajo')
    date = fields.Date('Fecha', default=fields.Date.today())
    sale = fields.Integer(string='Sueldo Base', related='contract_id.sale')
    bonus = fields.Integer(string='Bonificación Imponible')
    extra = fields.Integer(string='Horas Extras')
    gratuity = fields.Integer(string='Gratificación Legal', compute='_gratuity')
    afp = fields.Integer(string='AFP', compute='_afp')
    afp_id = fields.Float(string='Fondo AFP %', related='contract_id.afp_id')
    fonasa = fields.Integer(string='Fonasa', compute='_fonasa')
    sure = fields.Integer(string='Seguro de Cesantia', compute='_sure')
    tax = fields.Integer(string='Impuesto Unico')
    family = fields.Integer(string='Cargas Familiares')
    car = fields.Integer(string='Asignación Locomoción')
    lunch = fields.Integer(string='Asignación de Colación')

    taxi = fields.Integer(string='Haberes Imponibles', compute='_taxi')
    tax_id = fields.Integer(string='Haberes No Imponibles', compute='_tax_id')
    discount = fields.Integer(string='Descuentos', compute='_discount')
    pay = fields.Integer(string='Liquido a Pagar', compute='_pay')
    month = fields.Selection([('E', 'Enero'), ('F', 'Febrero'), ('M', 'Marzo'), ('A', 'Abril'), ('Z', 'Mayo'),
                              ('J', 'Junio'), ('X', 'Julio'), ('B', 'Agosto'), ('S', 'Septiembre'), ('O', 'Octubre'),
                              ('N', 'Noviembre'), ('D', 'Diciembre')], default='E')

    contract_id = fields.Many2one('hr.contract', string='Contracto', required=True)




    @api.depends('sale','bonus','extra')
    def _gratuity(self):
        for r in self:
            r.gratuity = 25*(r.sale+r.bonus+r.extra)/100

    @api.depends('sale','bonus','extra','gratuity')
    def _taxi(self):
        for r in self:
            r.taxi = r.sale+r.bonus+r.extra+r.gratuity

    @api.depends('family','car','lunch')
    def _tax_id(self):
        for r in self:
            r.tax_id = r.family+r.car+r.lunch

    @api.depends('taxi')
    def _sure(self):
        for r in self:
            r.sure =  6*r.taxi/1000

    @api.depends('taxi')
    def _fonasa(self):
        for r in self:
            r.fonasa = 7*r.taxi/100

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