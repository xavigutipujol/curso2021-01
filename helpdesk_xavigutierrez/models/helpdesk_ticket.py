import logging

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta

_logger = logging.getLogger(__name__)


class HelpdeskTicketAction(models.Model):
    _name = 'helpdesk.ticket.action'
    _description = 'Action'

    name = fields.Char()
    date = fields.Date()
    time = fields.Float(
        string='Time')
    ticket_id = fields.Many2one(
        comodel_name='helpdesk.ticket',
        string='Ticket')


class HelpdeskTicketTag(models.Model):
    _name = 'helpdesk.ticket.tag'
    _description = 'Tag'

    name = fields.Char()
    ticket_ids = fields.Many2many(
        comodel_name='helpdesk.ticket',
        relation='helpdesk_ticket_tag_rel',
        column1='tag_id',
        column2='ticked_id',
        string='Tickets')

    @api.model
    def cron_delete_tag(self):
        tickets = self.search([('ticket_ids', '=', False)])
        tickets.unlink()


class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _description = 'Ticket'

    def _date_default_today(self):
        return fields.Date.today()

    name = fields.Char(
        string='name',
        required=True)

    description = fields.Text(
        string='Description')

    date = fields.Date(
        string='Date',
        default=_date_default_today)

    state = fields.Selection(
        [('nuevo', 'Nuevoo'),
         ('asignado', 'Asignado'),
         ('proceso', 'En Proceso'),
         ('pendiente', 'Pendiente'),
         ('resuelto', 'Resuelto'),
         ('cancelado', 'Cancelado')],
        string='State',
        default='nuevo')
    time = fields.Float(
        string='Time',
        compute='_get_time',
        inverse='_set_time',
        search='_search_time')
    assigned = fields.Boolean(
        string='Assigned',
        compute='_compute_assigned')
    date_limit = fields.Date(
        string='Date Limit')
    action_corrective = fields.Html(
        string='Corrective Action',
        help='Description corrective action to do')
    action_preventive = fields.Html(
        string='Preventive Action',
        help='Description Preventive Action to do')

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Assigned to')

    tag_ids = fields.Many2many(
        comodel_name='helpdesk.ticket.tag',
        relation='helpdesk_ticket_tag_rel',
        column1='ticked_id',
        column2='tag_id',
        string='Tags')

    actions_ids = fields.One2many(
        comodel_name='helpdesk.ticket.action',
        inverse_name='ticket_id',
        string='Actions')

    @api.depends('actions_ids.time')
    def _get_time(self):
        for record in self:
            record.time = sum(record.actions_ids.mapped('time'))

    def _set_time(self):
        for record in self:
            if record.time:
                time_now = sum(record.actions_ids.mapped('time'))
                next_time = record.time - time_now
                if next_time:
                    data = {'name': '/', 'time': next_time,
                            'date': fields.Date.today(), 'ticket_id': record.id}
                    self.env['helpdesk.ticket.action'].create(data)

    def _search_time(self, operator, value):
        actions = self.env['helpdesk.ticket.action'].search(
            [('time', operator, value)])
        return [('id', 'in', actions.mapped('ticket_id').ids)]

    # Añadir en el header los siguiente botones:

    # - Asignar, cambia estado a asignado y pone a true el campo asignado, visible sólo con estado = nuevo
    def asignar(self):
        self.ensure_one()
        self.write({
            'state': 'asignado',
            'assigned': True})

    # - En proceso, visible sólo con estado = asignado

    def proceso(self):
        self.ensure_one()
        self.state = 'proceso'
    # - Pendiente, visible sólo con estado = en proceso o asignado

    def pendiente(self):
        self.ensure_one()
        self.state = 'pendiente'
    # - Finalizar, visible en cualquier estado, menos cancelado y finalizado

    def finalizado(self):
        self.ensure_one()
        self.state = 'resuelto'
    # - Cancelar, visible si no está cancelado

    def cancelado(self):
        self.ensure_one()
        self.state = 'cancelado'
    # Cada botón pondrá el objeto en el estado correspondiente.

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
            other_tickets = self.env['helpdesk.ticket'].search(
                [('user_id', '=', record.user_id.id)])
            record.ticket_qty = len(other_tickets)

    tag_name = fields.Char(
        string='Tag Name')

    def create_tag(self):
        self.ensure_one()
        # self.write({
        # 'tag_ids': [({'name': self.tag_name})]
        # })

        action = self.env.ref(
            'helpdesk_xavigutierrez.action_new_tag').read()[0]

        action['context'] = {
            'default_name': self.tag_name,
            'default_ticket_ids': [(6, 0, self.ids)]
        }
        #action['res_id'] = tag.id
        self.tag_name = False
        return action

    @api.constrains('time')
    def _time_positive(self):
        for ticket in self:
            if ticket.time and ticket.time < 0:
                raise ValidationError(_("The time can not be negative"))

    @api.onchange('date', 'date_limit')
    def _onchange_date(self):
        self.date_limit = self.date and self.date + timedelta(days=1)
