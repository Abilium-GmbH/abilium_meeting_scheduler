# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api
from typing import List
from datetime import datetime


class group_scheduler(models.Model):
    _name = 'group_scheduler'
    _description = 'group_scheduler'

    meeting_group = fields.Char(string="Meeting Group", required=True)
    meeting_attendees = fields.Many2many('res.users', string="Attendees") #todo partners

    # those variables need to apear in a search form
    # meeting_search_start_date = fields.Datetime(string="Search Start Date", required=True)
    # meeting_search_end_date = fields.Datetime(string="Search End Date", required=True)

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
        # self.env['print_table'].create({'show_stuff': partner_id_list})

    # get related calendar_event_id from  calendar_event_res_partner_rel
    # get related meetings from calendar_event
        meeting_found = self.env['calendar.event'].search([])
        meeting_selected_list = []
        for ting in meeting_found:
            for uid in partner_id_list: #group_res_users_all_ids:
                for pflopf in ting.attendee_ids.partner_id:
                    if(uid == pflopf.id):
                        meeting_selected_list.append(ting)
                        # self.env['print_table'].create({'show_stuff': str(ting.name) + ', ' + str(ting.start) + ', ' + str(ting.attendee_ids.partner_id)})
        meeting_selected_list = list(dict.fromkeys(meeting_selected_list))
        meeting_start_end_list = []
        for x in meeting_selected_list:
            meeting_start_end_list.append([x.start, x.stop])
            # self.env['print_table'].create(
            #     {'show_stuff': str(x.name) + ', '
            #                    + str(x.start) + ', '
            #                    + str(x.stop) + ', '
            #                    + str(x.attendee_ids.partner_id)})

        result = self.find_overlapping_timeslots(meeting_start_end_list)
        # timeslots = [[datetime(2023, 3, 29, 10, 0), datetime(2023, 3, 29, 12, 0)],
        #              [datetime(2023, 3, 29, 11, 0), datetime(2023, 3, 29, 13, 0)],
        #              [datetime(2023, 3, 29, 14, 0), datetime(2023, 3, 29, 15, 0)],
        #              ]
        # result = self.find_overlapping_timeslots(timeslots)
        self.env['print_table'].create(
            {'show_stuff': result})

    def find_overlapping_timeslots(self, timeslots: List[List[datetime]]) -> List[List[datetime]]:
        """
        Given a list of timeslots represented as a list of start and end times,
        returns a list of overlapping timeslots.
        """
        overlaps = []
        for i in range(len(timeslots)):
            for j in range(i + 1, len(timeslots)):
                # check if the two timeslots overlap
                if timeslots[i][0] < timeslots[j][1] and timeslots[i][1] > timeslots[j][0]:
                    # add the overlapping timeslot to the list of overlaps
                    overlap_start = max(timeslots[i][0], timeslots[j][0])
                    overlap_start_converted = self.convert_timezone(overlap_start)

                    overlap_end = min(timeslots[i][1], timeslots[j][1])
                    overlap_end_converted = self.convert_timezone(overlap_end)

                    overlaps.append([overlap_start_converted, overlap_end_converted])

        for overlap in overlaps:
            otuput_overlaps = overlap[0] , overlap[1]
        return otuput_overlaps

    def convert_timezone(self, input_datetime: datetime) -> datetime:
        import pytz
        user_timezone = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
        output_datetime = pytz.utc.localize(input_datetime).astimezone(user_timezone)
        return output_datetime

