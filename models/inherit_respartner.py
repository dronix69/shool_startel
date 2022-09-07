import datetime
from odoo import fields, models, api
from odoo.exceptions import ValidationError
import re

class NewResPartner(models.Model):
    _inherit = 'res.partner'

    educa = fields.Selection(
        [('B', 'Basica Completa'), ('N', 'Media Incompleta'), ('C', 'Media Completa'), ('S', 'Superior')],
        string='Nivel Educacional')
    jornal = fields.Selection(
        [('j_mañana', 'Jornada Mañana'), ('j_tarde', 'Jornada Tarde'), ('vespertino', 'Vespertino'),
         ('f_semana', 'Fin de Semana')],
        string='Jonarda')
    date_ids = fields.Date('Fecha Matricula', default=fields.Date.today())
    student = fields.Many2one('cert.cursos', string='Nº Curso')
    curso_ids = fields.Char('Curso')
    student_count = fields.Integer(string="Total Practicas", compute="compute_student_count")

    def get_cert(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name' : 'Certificados',
            'view_mode' : 'tree',
            'res_model' : 'certificados.cert',
            'domain' : [('name', '=', self.id)],
            'context' : "{'create': False}"
        }

    def compute_student_count(self):
        for record in self:
            record.student_count = self.env['certificados.cert'].search_count([('name', '=', self.id)])

    @api.onchange('student')
    def _onchange_student(self):
        for record in self:
            if record.student:
                record.curso_ids = record.student.number

    @api.constrains('phone')
    def validate_phone(self):
        for rec in self:
            if rec.phone:
                if len(rec.phone) < 6 or re.match(r"^[a-zA-Z][a-zA-Z]*", rec.phone):
                    raise ValidationError('El nùmero de telefono no puede contener letras')

    @api.constrains('email')
    def validate_email(self):
        for rec in self:
            if rec.email:
                if not re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", rec.email):
                    raise ValidationError('Error en formato del correo')

    
class NacPartner(models.Model):
    _inherit = 'res.partner'

    bdate = fields.Date(string='Fecha de Nacimiento', required=True)
    student_age = fields.Integer(string='Edad', compute='_get_age_from_student')


    @api.depends('bdate')
    def _get_age_from_student(self):
        today_date = datetime.date.today()
        for stud in self:
            if stud.bdate:
                bdate = fields.Datetime.to_datetime(stud.bdate).date()
                total_age = str(int((today_date - bdate).days / 365))
                stud.student_age = total_age
            else:
                stud.student_age = 'No Provisto...'

