# -*- coding: utf-8 -*-

from odoo import models, fields, api

# Tutorial see here
# https://www.cybrosys.com/blog/add-settings-menu-custom-modules-in-odoo

class ResConfigSettings(models.TransientModel):
   _inherit = 'res.config.settings'
   base_salary = fields.Integer("Salary")
