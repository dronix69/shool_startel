from odoo import fields, models


class  CertSaleOrder(models.Model):
    _inherit = 'sale.order'

    boleta = fields.Char('Boleta Transbank', required=True)
    ticket_id = fields.Selection(
        [('D', 'Debito'), ('C', 'Credito'), ('K', 'Comercial'),
         ('E', 'Efectivo')], string='Medio de Pago')
    


class HrContract(models.Model):
    _inherit = 'hr.contract'
    _description = 'Employee Contract'


    sale = fields.Integer(string='Sueldo Base', required=True)
    afp = fields.Selection(
        [('capital', 'Capital'), ('cuprum', 'Cuprum'), ('habitatK', 'Habitat'),
         ('vital', 'P Vital'), ('provida', 'Provida'), ('modelo', 'Modelo'), ('uno', 'Uno') ], string='AFP')
    afp_id = fields.Float(string='Fondo AFP', required=True)




