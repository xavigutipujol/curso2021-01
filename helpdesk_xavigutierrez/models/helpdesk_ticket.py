from odoo import models, fields

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
        readonly = True)
    date_limit = fields.Date(
        string = 'Date Limit')
    action_corrective = fields.Html(
        string = 'Corrective Action',
        help = 'Description corrective action to do')
    action_preventive = fields.Html(
        string = 'Preventive Action',
        help = 'Description Preventive Action to do')

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