import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class HelpdeskTicketAction(models.Model):
    _name = 'helpdesk.ticket.action'
    _description = 'Action'

    name = fields.Char()
    date = fields.Date()
    ticket_id = fields.Many2one(
        comodel_name = 'helpdesk.ticket',
        string = 'Ticket')

class HelpdeskTicketTag(models.Model):
    _name = 'helpdesk.ticket.tag'
    _description = 'Tag'

    name = fields.Char()
    ticket_ids = fields.Many2many(
        comodel_name = 'helpdesk.ticket',
        relation = 'helpdesk_ticket_tag_rel',
        column1 = 'tag_id',
        column2 = 'ticked_id',
        string = 'Tickets')

class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _description = 'Ticket'
    
    name = fields.Char(
        string='name',
        required = True)
    
    description = fields.Text(
        string='Description')

    date = fields.Date(
        string='Date')

    state = fields.Selection(
        [('nuevo', 'Nuevoo'),
         ('asignado', 'Asignado'),
         ('proceso', 'En Proceso'),
         ('pendiente', 'Pendiente'),
         ('resuelto', 'Resuelto'),
         ('cancelado', 'Cancelado')],
        string = 'State',
        default = 'nuevo')
    time = fields.Float(
        string = 'Time')
    assigned = fields.Boolean(
        string = 'Assigned',
        compute = '_compute_assigned')
    date_limit = fields.Date(
        string = 'Date Limit')
    action_corrective = fields.Html(
        string = 'Corrective Action',
        help = 'Description corrective action to do')
    action_preventive = fields.Html(
        string = 'Preventive Action',
        help = 'Description Preventive Action to do')

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Assigned to')

    tag_ids = fields.Many2many(
        comodel_name = 'helpdesk.ticket.tag',
        relation = 'helpdesk_ticket_tag_rel',
        column1 = 'ticked_id',
        column2 = 'tag_id',
        string = 'Tags')

    actions_ids = fields.One2many(
        comodel_name = 'helpdesk.ticket.action',
        inverse_name = 'ticket_id',
        string = 'Actions')

    #Añadir en el header los siguiente botones:

    #- Asignar, cambia estado a asignado y pone a true el campo asignado, visible sólo con estado = nuevo
    def asignar(self):
        self.ensure_one()
        self.write({
           'state': 'asignado',
           'assigned': True})
        

    #- En proceso, visible sólo con estado = asignado

    def proceso(self):
        self.ensure_one()
        self.state = 'proceso'
    #- Pendiente, visible sólo con estado = en proceso o asignado
    def pendiente(self):
        self.ensure_one()
        self.state = 'pendiente'
    #- Finalizar, visible en cualquier estado, menos cancelado y finalizado
    def finalizado(self):
        self.ensure_one()
        self.state = 'resuelto'
    #- Cancelar, visible si no está cancelado
    def cancelado(self):
        self.ensure_one()
        self.state = 'cancelado'
    #Cada botón pondrá el objeto en el estado correspondiente.
    @api.depends('user_id')
    def _compute_assigned(self):
        for record in self:
            record.assigned = self.user_id and True or False

    ticket_qty = fields.Integer(
        string='Ticket Qty',
        compute='_compute_ticket_qty')

    @api.depends('user_id')
    def _compute_ticket_qty(self):
        for record in self:
            other_tickets = self.env['helpdesk.ticket'].search([('user_id', '=', record.user_id.id)])
            record.ticket_qty = len(other_tickets)
    
    tag_name = fields.Char(
        string='Tag Name')

    def create_tag(self):
        self.write({
            'tag_ids': [({'name': self.tag_name})]
        })