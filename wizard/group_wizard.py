# -*- coding: utf-8 -*-

from odoo import models, fields, api
from typing import List
from datetime import datetime


class group_wizard(models.TransientModel):
    _name = 'group_wizard'
    _description = 'group_wizard'
    # _inherit = 'meeting_scheduler.group_scheduler'

    search_start_date = fields.Date(string="Search Start Date", required=False)
    search_end_date = fields.Date(string="Search End Date", required=False)
    working_hour_start = fields.Float(string="Working hour Start", default=08.00, required=False)
    working_hour_end = fields.Float(string="Working hour End", default=17.00, required=False)

    # @api.model_create_multi
    def method_a(self):
        return  self.env['group_scheduler'].button_function_test()
        # return True
