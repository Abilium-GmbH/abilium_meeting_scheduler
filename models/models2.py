# -*- coding: utf-8 -*-
import datetime

import pytz

from odoo import models, fields, api
from typing import List
from datetime import datetime, timedelta
import math


class group_scheduler(models.Model):
    _name = 'group_scheduler'
    _description = 'group_scheduler'

    meeting_group = fields.Char(string="Meeting Group", required=True)
    meeting_attendees = fields.Many2many('res.users', string="Attendees")

    def open_time_form(self):
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'group_wizard',  # name of respective model,
            # 'views': [('group_scheduler_timeform', 'form')],  # view id and type
            'view_id': self.env.ref('meeting_scheduler.group_scheduler_timeform').id,  # view id
            'target': 'new',
            # 'context': context,
        }

    def transform_meetings_to_bookable_hours(self, meetings):
        """
        TODO
        :param meetings is a list of following shape [datetime startdate, datetime enddate, list[user id]]:
        :return: output_timeslots a list of following objects [string startdate,
                                                                string enddate,
                                                                list[string bookable_hours],
                                                                datetime startdate,
                                                                datetime enddate]
        """
        output_timeslots = []
        for meeting in meetings:
            duration = meeting[1] - meeting[0]
            duration = math.floor(duration.total_seconds() / 3600)
            bookable_hours = ""
            for i in range(meeting[0].hour, meeting[0].hour + duration + 2):
                bookable_hours += " " + str(i)  # the list has to be treated as a string,
                # # so that the t-foreach from the qweb template can interpret it as a list
            output_timeslots.append([str(self.convert_timezone(meeting[0])),
                                     #           (meeting[0].strftime('%Y-%m-%d, %Z')),
                                     str(self.convert_timezone(meeting[1])),
                                     bookable_hours,
                                     meeting[0],
                                     meeting[1],
                                     meeting[2]])
        return output_timeslots

    def convert_timezone(self, input_datetime: datetime) -> datetime:
        import pytz
        user_timezone = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
        output_datetime = pytz.utc.localize(input_datetime).astimezone(user_timezone)
        output_datetime = output_datetime.replace(tzinfo=None)  # removes the +2:00 from utc
        # self.env['print_table'].create({'show_stuff': pytz.utc.localize(output_datetime)})

        """
        suggested solution

        First we get the users timezone for some comparisons:
            1. If the tz of the input_datetime is None then dont convert anything
            2. Otherwise convert from old tz to new tz
        """
        # user_timezone = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
        #
        # if input_datetime.tzname() is None:
        #     output_datetime = input_datetime
        #
        # else:
        #     output_datetime = input_datetime.astimezone(user_timezone)
        #     output_datetime = output_datetime.replace(tzinfo=None)

        return output_datetime

    def button_timeslots_from_intersection(self,
                                           search_start_date,
                                           search_end_date):
        group_selected_ids = self.env.context.get('active_ids', [])
        group_selected_records = self.env['group_scheduler'].browse(group_selected_ids)  # get ids from group members
        group_res_users_all_ids = []
        # this for-loop iterates over the selected groups
        for group in group_selected_records:
            # this for-loop iterates over the group members
            # group_scheduler_res_users_rel has user ids and group ids
            for group_member in group.meeting_attendees:
                group_res_users_all_ids.append(group_member['id'])
        group_res_users_all_ids = list(dict.fromkeys(group_res_users_all_ids))
        # partner_id NOT EQUAL to user_id!!
        self.generate_intersection(group_res_users_all_ids, search_start_date, search_end_date)

    def generate_intersection(self, group_res_users_all_ids, search_start_date, search_end_date):
        found_meetings_per_group_member = []
        for group_member in group_res_users_all_ids:
            meetings_found = self.env['meeting_scheduler'].search(['&',
                                                                   ('meeting_start_date', '>=',
                                                                    search_start_date),
                                                                   ('meeting_end_date', '<=',
                                                                    search_end_date),
                                                                   ('create_uid', '=', group_member)])
            found_meetings_per_group_member.append(meetings_found)
        # if zero not needed because we do not return as in a function, we directly create
        if (len(group_res_users_all_ids) == 1):
            timeslots_bookable_h = self.transform_meetings_to_bookable_hours(found_meetings_per_group_member[0])
            for i in timeslots_bookable_h:
                self.env['timeslots'].create({'timeslots_start_date_str': i[0],
                                              'timeslots_end_date_str': i[1],
                                              'timeslots_bookable_hours': i[2],
                                              'timeslots_start_date_utc': i[3],
                                              'timeslots_end_date_utc': i[4],
                                              'timeslots_groupmembers': i[5]})
        elif (len(group_res_users_all_ids) > 1):
            free_meetings_list = []
            for first_user in found_meetings_per_group_member[0]:
                free_meetings_list.append([first_user.meeting_start_date, first_user.meeting_end_date])
            for all_other_users in found_meetings_per_group_member[1:]:
                free_meetings_list_temp = []
                for meeting in all_other_users:
                    for index_free, free_meeting in enumerate(free_meetings_list):
                        meeting_starttime = meeting.meeting_start_date
                        meeting_endtime = meeting.meeting_end_date
                        free_starttime = free_meeting[0]
                        free_endtime = free_meeting[1]

                        if (free_starttime <= meeting_starttime) \
                                and (meeting_starttime <= free_endtime) \
                                and (free_starttime <= meeting_endtime) \
                                and (free_endtime <= meeting_endtime):
                            # case 1, meeting starts before freetime ends
                            free_meetings_list_temp.append([meeting_starttime, free_endtime])

                        elif (meeting_starttime <= free_starttime) \
                                and (meeting_starttime <= free_endtime) \
                                and (free_starttime <= meeting_endtime) \
                                and (meeting_endtime <= free_endtime):
                            # case 2, meeting ends after freetime starts
                            free_meetings_list_temp.append([free_starttime, meeting_endtime])

                        elif (free_starttime < meeting_starttime) \
                                and (meeting_starttime < free_endtime) \
                                and (free_starttime < meeting_endtime) \
                                and (meeting_endtime < free_endtime):
                            # case 3, meeting lies between free time
                            free_meetings_list_temp.append([meeting_starttime, meeting_endtime])

                        elif (meeting_starttime <= free_starttime) \
                                and (meeting_starttime <= free_endtime) \
                                and (free_starttime <= meeting_endtime) \
                                and (free_endtime <= meeting_endtime):
                            # case 4, freetime lies between meeting, delete
                            free_meetings_list_temp.append([free_starttime, free_endtime])

                free_meetings_list = free_meetings_list_temp
            intersecting_meetings = []
            for j in free_meetings_list:
                intersecting_meetings.append([j[0], j[1], group_res_users_all_ids])
            timeslots_bookable_h = self.transform_meetings_to_bookable_hours(intersecting_meetings)
            for i in timeslots_bookable_h:
                self.env['timeslots'].create({'timeslots_start_date_str': i[0],
                                              'timeslots_end_date_str': i[1],
                                              'timeslots_bookable_hours': i[2],
                                              'timeslots_start_date_utc': i[3],
                                              'timeslots_end_date_utc': i[4],
                                              'timeslots_groupmembers': i[5]})
                # self.env['print_table'].create({'show_stuff': i})

    def button_timeslots_from_union(self,
                                    search_start_date,
                                    search_end_date):
        group_selected_ids = self.env.context.get('active_ids', [])
        group_selected_records = self.env['group_scheduler'].browse(group_selected_ids)  # get ids from group members
        group_res_users_all_ids = []
        # this for-loop iterates over the selected groups
        for group in group_selected_records:
            # this for-loop iterates over the group members
            # group_scheduler_res_users_rel has user ids and group ids
            for group_member in group.meeting_attendees:
                group_res_users_all_ids.append(group_member['id'])
        group_res_users_all_ids = list(dict.fromkeys(group_res_users_all_ids))
        # partner_id NOT EQUAL to user_id!!
        self.generate_union(group_res_users_all_ids, search_start_date, search_end_date)

    def generate_union(self, group_res_users_all_ids, search_start_date, search_end_date):
        found_meetings_per_group_member = []
        for group_member in group_res_users_all_ids:
            meetings_found = self.env['meeting_scheduler'].search(['&',
                                                                   ('meeting_start_date', '>=',
                                                                    search_start_date),
                                                                   ('meeting_end_date', '<=',
                                                                    search_end_date),
                                                                   ('create_uid', '=', group_member)])
            for meeting_found in meetings_found:
                found_meetings_per_group_member.append([meeting_found.meeting_start_date,
                                                        meeting_found.meeting_end_date,
                                                        [group_member]])

        timeslots_bookable_h = self.transform_meetings_to_bookable_hours(found_meetings_per_group_member)
        for i in timeslots_bookable_h:
            self.env['timeslots'].create({'timeslots_start_date_str': i[0],
                                          'timeslots_end_date_str': i[1],
                                          'timeslots_bookable_hours': i[2],
                                          'timeslots_start_date_utc': i[3],
                                          'timeslots_end_date_utc': i[4],
                                          'timeslots_groupmembers': i[5]})
            # self.env['print_table'].create({'show_stuff': i})
