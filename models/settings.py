# -*- coding: utf-8 -*-

from odoo import models, fields, api

# Tutorial see here
# https://www.cybrosys.com/blog/add-settings-menu-custom-modules-in-odoo

class ResConfigSettings(models.TransientModel):
   _inherit = 'res.config.settings'
   base_salary = fields.Integer("Salary")
   meeting_title_default = fields.Char(string="Meeting Title Default", default="TimeForCustomerMeeting")
   locktime_hours_default = fields.Integer(string="Locktime Hours Default", default="24")

   def set_values(self):
       """meeting_scheduler setting field values"""
       res = super(ResConfigSettings, self).set_values()
       self.env['ir.config_parameter'].set_param('meeting_scheduler.base_salary', self.base_salary)
       self.env['ir.config_parameter'].set_param('meeting_scheduler.meeting_title_default', self.meeting_title_default)
       self.env['ir.config_parameter'].set_param('meeting_scheduler.locktime_hours_default', self.locktime_hours_default)
       return res
   def get_values(self):
       """meeting_scheduler limit getting field values"""
       res = super(ResConfigSettings, self).get_values()
       value_base_salary = self.env['ir.config_parameter'].sudo().get_param('employee_department.base_salary')
       value_meeting_title_default = self.env['ir.config_parameter'].sudo().get_param('meeting_scheduler.meeting_title_default')
       value_locktime_hours_default = self.env['ir.config_parameter'].sudo().get_param('meeting_scheduler.locktime_hours_default')
       res.update(
            base_salary=float(value_base_salary),
            meeting_title_default = str(value_meeting_title_default),
            locktime_hours_default = int(value_locktime_hours_default)
       )
       return res
