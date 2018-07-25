# - coding: utf-8 -*-
from odoo import models, fields, api
from odoo import exceptions
import logging

_logger = logging.getLogger(__name__)

class TodoWizard(models.TransientModel):
    _name = 'todo.wizard'
    _description = 'To-do Mass Assignment'
    task_ids = fields.Many2many('todo.task',
        string='Tasks')
    new_deadline = fields.Date('Deadline to Set')
    new_user_id = fields.Many2one(
        'res.users', string='Responsible to Set')


    @api.multi
    def do_mass_update(self):
        # handle one wizard instance at a time, to make that clear
        self.ensure_one()
        #########################

        if not (self.new_deadline or self.new_user_id.id):
            raise exceptions.ValidationError('No data to update!')

        # _logger.debug(' A DEBUG message')
        # _logger.info(' An INFO message')
        # _logger.warning(' A WARNING message')
        # _logger.error(' An ERROR message')

        _logger.debug('Mass update on Todo Tasks %s',
                    self.task_ids.ids)
        vals= {}
        if self.new_deadline:
            vals['date_deadline'] = self.new_deadline
        if self.new_user_id.id:
            vals['user_id'] = self.new_user_id.id
        
        # Mass write alues on all selected tasks
        
        if vals:
            self.task_ids.write(vals)
        return True

    @api.multi
    def do_count_tasks(self):
        Task = self.env['todo.task']
        count = Task.search_count([('is_done', '=', False)])
        raise exceptions.Warning(
            'There are %d active tasks.' %count)

    # for select all and still keep same wizard
    ################################################
    @api.multi
    def _reopen_form(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name, #this model
            'res_id': self.id, #the current wizard record
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new'}

    @api.multi
    def do_populate_tasks(self):
        self.ensure_one()
        Task = self.env['todo.task']
        open_tasks = Task.search([('is_done', '=', False)])
        # Fill the wizard Task list with all tasks
        self.task_ids = open_tasks
        # reopen wizard form on same wizard record
        return self._reopen_form()

    ################################################

    # @api.model
    # def create(self, vals):
    #     # Code before create: can use the vals dict
    #     new_record = super(TodoTask, self).create(vals)
    #     # Code before create: can use the new_record created
    #     return new_record

    # @api.multi
    # def write(self, vals):
    #     # Code before write: can use the self, with the old values
    #     super(TodoTask, self).write(vals)
    #     # Code after write: can use the self, with the updated values
    #     return True