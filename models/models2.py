# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api


class group_scheduler(models.Model):
    _name = 'group_scheduler'
    _description = 'group_scheduler'

    meeting_group = fields.Char(string="Meeting Group", required=True)
    meeting_attendees = fields.Many2many('res.users', string="Attendees")

    def button_function_test(self):
        group_selected_ids = self.env.context.get('active_ids', [])
        group_selected_records = self.env['group_scheduler'].browse(group_selected_ids)
    # get ids from group members
        group_res_users_all_ids = []
        # this for-loop iterates over the selected groups
        for group in group_selected_records:
            # this for-loop iterates over the group members
    # group_scheduler_res_users_rel has user ids and group ids
            for group_member in group.meeting_attendees:
                group_res_users_all_ids.append(group_member['id'])
        group_res_users_all_ids = list(dict.fromkeys(group_res_users_all_ids))
    # partner_id NOT EQUAL to user_id!!
    # get partner_id from res_users
        partner_id_records = self.env['res.users'].browse(group_res_users_all_ids)
        partner_id_list = []
        for partners in partner_id_records:
            for partner_id_entry in partners['partner_id']:
                partner_id_list.append(partner_id_entry['id'])
        self.env['print_table'].create({'show_stuff': partner_id_list})

    # get related calendar_event_id from  calendar_event_res_partner_rel
    #     meeting_found = self.env['calendar.event.res.partner.rel'].search([('res_partner_id', '=', 2)])
    #     for meeting_entry in meeting_found:
    #         self.env['print_table'].create({'show_stuff': meeting_entry})

    # get related meetings from calendar_event
    # calc freetime with stardate enddate



