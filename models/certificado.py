from odoo import api, fields, models
import datetime


class Cert(models.Model):
    _name = 'certificados.cert'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = ' Registro de Certificado'

    def action_confirm(self):
        for rec in self:
            rec.state = 'C'

    def action_done(self):
        for rec in self:
            rec.state = 'B'

    def action_print(self):
        for rec in self:
            rec.state = 'C'
            return self.env.ref('shool_startel.reporte_certificado_cert').report_action(self)

    name = fields.Many2one('res.partner', required=True)
    customer = fields.Char(string='Rut', related='name.vat')
    number = fields.Selection([('BO', 'BO'), ('BP', 'BP'), ('A2', 'A2'), ('A3', 'A3'), ('A4', 'A4'), ('A5', 'A5'),
                               ('A2-A4', 'A2-A4'), ('A3-A5', 'A3-A5')], string='Tipo Contrato',
                              related='curso_id.number')
    codigo = fields.Char(string='Codigo Curso', related='curso_id.codigo')
    curso_id = fields.Many2one('cert.cursos', required=True)
    date_1 = fields.Date(string='Fecha Inicio', default=fields.Date.today())
    date_2 = fields.Date(string='Fecha Fin')
    certi = fields.Char(string='N Certificado')
    fact = fields.Char(string='N Factura Cert')
    image = fields.Binary(string='Imagen')
    state = fields.Selection([('A', 'Procesando'), ('B', 'Con Deuda'), ('C', 'Entregado')], default='A')
    progress = fields.Integer(string="Progreso", compute="_compute_progress")

    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'A':
                progress = 25
            elif rec.state == 'B':
                progress = 50
            elif rec.state == 'C':
                progress = 100
            else:
                progress = 0
            rec.progress = progress

