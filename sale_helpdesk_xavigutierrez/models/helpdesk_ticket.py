from odoo import models, api, fields, _


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    sale_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sale Order')
