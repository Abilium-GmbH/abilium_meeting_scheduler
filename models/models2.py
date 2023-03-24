# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api


class group_scheduler(models.Model):
    _name = 'group_scheduler'
    _description = 'group_scheduler'

    meeting_group = fields.Char(string="Meeting Group", required=True)
    meeting_attendees = fields.Many2many('res.users', string="Attendees")

    def button_function_test(self):
        grouplist = self
        # grouplist.meeting_attendees.
# get ids from group members
# partner_id NOT EQUAL to user_id!!
# group_scheduler_res_users_rel has user ids and group ids
# get partner_id from res_users
# get related calendar_event_id from  calendar_event_res_partner_rel
# get related meetings from calendar_event
# calc freetime with stardate enddate