from odoo import fields, models


class  CertSaleOrder(models.Model):
    _inherit = 'sale.order'

    boleta = fields.Char('Boleta Transbank', required=True)
    ticket_id = fields.Selection(
        [('D', 'Debito'), ('C', 'Credito'), ('K', 'Comercial'),
         ('E', 'Efectivo')], string='Medio de Pago')
    



