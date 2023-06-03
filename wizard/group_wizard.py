# -*- coding: utf-8 -*-

from odoo import models, fields, api
from typing import List
from datetime import datetime


class group_wizard(models.TransientModel):
    _name = 'group_wizard'
    _description = 'group_wizard'

    search_start_date = fields.Date(string="Search Start Date", required=True,
                                    default=lambda self: fields.datetime.now())
    search_end_date = fields.Date(string="Search End Date", required=True,
                                  default=lambda self: fields.datetime.now())

    #TODO check that search_start_date is before search_end_date, same for working hour

    # @api.model_create_multi
    def transit_button_timeslots_from_intersection(self):
        for record in self:
            return  self.env['group_scheduler'].button_timeslots_from_intersection(record.search_start_date,
                                                                     record.search_end_date)
        # return True

    def transit_button_timeslots_from_union(self):
        for record in self:
            return self.env['group_scheduler'].button_timeslots_from_union(record.search_start_date,
                                                                        record.search_end_date)


