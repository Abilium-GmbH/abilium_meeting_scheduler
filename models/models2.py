# -*- coding: utf-8 -*-
import datetime

import pytz

from odoo import models, fields, api
from typing import List
from datetime import datetime, timedelta



class group_scheduler(models.Model):
    _name = 'group_scheduler'
    _description = 'group_scheduler'

    meeting_group = fields.Char(string="Meeting Group", required=True)
    meeting_attendees = fields.Many2many('res.users', string="Attendees") #todo partners

    # TODO those variables need to apear in a search form
    # meeting_search_start_date = fields.Datetime(string="Search Start Date", required=True)
    # meeting_search_end_date = fields.Datetime(string="Search End Date", required=True)

    def button_timeslots_from_intersection(self,
                             search_start_date,
                             search_end_date,
                             working_hour_start,
                             working_hour_end):
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

        found_meetings_per_group_member = []
        for group_member in group_res_users_all_ids:
            meetings_found = self.env['meeting_scheduler'].search(['&',
                                                              ('meeting_start_date', '>=',
                                                               search_start_date),
                                                              ('meeting_end_date', '<=',
                                                               search_end_date),
                                                                  ('create_uid', '=', group_member)])
            found_meetings_per_group_member.append(meetings_found)
        self.env['print_table'].create({'show_stuff': len(group_res_users_all_ids)})

        # if zero not needed because we do not return only create
        # if(len(group_res_users_all_ids) == 0):
        #     self.env['print_table'].create({'show_stuff': "no user empty list"})
        #     return []
        if(len(group_res_users_all_ids) == 1):
            self.env['print_table'].create({'show_stuff': len(group_res_users_all_ids)})
            timeslots_bookable_h = self.transform_meetings_to_bookable_hours(found_meetings_per_group_member[0])
            for i in timeslots_bookable_h:
                self.env['timeslots'].create({'timeslots_start_date': i[0],
                                              'timeslots_end_date': i[1],
                                              'timeslots_bookable_hours': i[2]})
        elif (len(group_res_users_all_ids) > 1):
            free_meetings_list = []
            for first_user in found_meetings_per_group_member[0]:
                free_meetings_list.append([first_user.meeting_start_date, first_user.meeting_end_date])
            self.env['print_table'].create({'show_stuff': "after filling"})
            self.env['print_table'].create({'show_stuff': free_meetings_list})

            for all_other_users in found_meetings_per_group_member[1:]:
                free_meetings_list_temp = []
                for meeting in all_other_users:
                    for index_free, free_meeting in enumerate(free_meetings_list):
                        # meeting_starttime = self.convert_timezone(meeting.meeting_start_date)
                        # meeting_endtime = self.convert_timezone(meeting.meeting_end_date)
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

            self.env['print_table'].create({'show_stuff': free_meetings_list})

    def transform_meetings_to_bookable_hours(self, meetings):
        """
        TODO
        :param meetings is a list of following objects [meeting_scheduler objects for user x]:
        :return: output_timeslots a list of following objects [string startdate,
                                                                string enddate,
                                                                list[string bookable_hours],
                                                                datetime startdate,
                                                                datetime enddate]
        """
        import math
        output_timeslots = []
        for meeting in meetings:
            duration = meeting.meeting_end_date - meeting.meeting_start_date
            duration = math.floor(duration.total_seconds() / 3600)
            bookable_hours = ""
            for i in range(meeting.meeting_start_date.hour, meeting.meeting_start_date.hour+duration+1):
                bookable_hours += " " + str(i) # the list has to be treated as a string,
                # # so that the t-foreach from the qweb template can interpret it as a list
            output_timeslots.append([str(meeting.meeting_start_date),
                                     str(meeting.meeting_end_date),
                                     bookable_hours,
                                     meeting.meeting_start_date,
                                     meeting.meeting_end_date
                                     ])
        return output_timeslots

    def calc_bookable_hours(self, timeslots):
        import math
        output_timeslots = []
        for timeslot in timeslots:
            duration = timeslot[1] - timeslot[0]
            duration = math.floor(duration.total_seconds() / 3600)
            bookable_hours = ""
            for i in range(timeslot[0].hour, timeslot[0].hour+duration+1):
                bookable_hours += " " + str(i) # the list has to be treated as a string,
                # # so that the t-foreach from the qweb template can interpret it as a list
            output_timeslots.append([timeslot[0], timeslot[1], bookable_hours])
        return output_timeslots



    # def open_time_form(self, cr, uid, ids, context=None):
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

    def button_timeslots_from_union(self,
                             search_start_date,
                             search_end_date,
                             working_hour_start,
                             working_hour_end):
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
        # self.env['print_table'].create({'show_stuff': group_res_users_all_ids})
    # partner_id NOT EQUAL to user_id!!
    # get partner_id from res_users
    #     partner_id_records = self.env['res.users'].browse(group_res_users_all_ids)
    #     partner_id_list = []
    #     for partners in partner_id_records:
    #         for partner_id_entry in partners['partner_id']:
    #             partner_id_list.append(partner_id_entry['id'])
        # self.env['print_table'].create({'show_stuff': partner_id_list})

    # get related calendar_event_id from  calendar_event_res_partner_rel
    # get related meetings from calendar_event
        day_difference = int((search_end_date - search_start_date).days)
        daily_meetings_sorted = []
        for i in range(0, day_difference+1):
            self.env['print_table'].create({'show_stuff': search_start_date + timedelta(days=i)})
            meeting_found = self.env['meeting_scheduler'].search(['&',
                                                               ('meeting_start_date', '>=', search_start_date + timedelta(days=i)),
                                                               ('meeting_end_date', '<=', search_start_date + timedelta(days=i))])
            meeting_selected_list = []
            for ting in meeting_found:
                for uid in group_res_users_all_ids: #group_res_users_all_ids:
                    for pflopf in ting.create_uid:
                        if(uid == pflopf.id):
                            meeting_selected_list.append(ting)
                            # self.env['print_table'].create({'show_stuff': str(ting.name) + ', ' + str(ting.start) + ', ' + str(ting.attendee_ids.partner_id)})
            meeting_selected_list = list(dict.fromkeys(meeting_selected_list))
            meeting_start_end_list = []
            for x in meeting_selected_list:
                meeting_start_end_list.append([x.id, x.meeting_start_date, x.meeting_end_date, x.meeting_duration])

            daily_meetings_temp = self.alg02(meeting_start_end_list,
                                                  (search_start_date + timedelta(days=i)),
                                                  (search_start_date + timedelta(days=i)),
                                                 working_hour_start,
                                                 working_hour_end)
            for x in daily_meetings_temp:
                daily_meetings_sorted.append(x)
            self.env['print_table'].create({'show_stuff': daily_meetings_sorted})

        timeslots_bookable_h = self.calc_bookable_hours(daily_meetings_sorted)
        # self.env['print_table'].create({'show_stuff': timeslots_bookable_h})
        for i in timeslots_bookable_h:
            self.env['timeslots'].create({'timeslots_start_date': i[0],
                                          'timeslots_end_date': i[1],
                                          'timeslots_bookable_hours': i[2]})

    def alg02(self, meetings, search_start_date, search_end_date, working_hour_start, working_hour_end):
        import pytz
        import math
        whs_min_float, whs_hour_float = math.modf(working_hour_start)
        working_hours_start = datetime(year=search_start_date.year,
                                       month=search_start_date.month,
                                       day=search_start_date.day,
                                       hour=int(whs_hour_float),
                                       minute=int(whs_min_float*60), second=0)
                                        # TODO get from odoo and give to function
        # working_hours_start = self.convert_timezone(working_hours_start) #not needed if defined with float_time
        whe_min_float, whe_hour_float = math.modf(working_hour_end)

        working_hours_end = datetime(year=search_end_date.year,
                                     month=search_end_date.month,
                                     day=search_end_date.day,
                                     hour=int(whe_hour_float), minute=int(whe_min_float*60),
                                     second=0)  # TODO get from odoo and give to function
        # working_hours_end = self.convert_timezone(working_hours_end)
        meetings_sorted_duration = sorted(meetings, key=lambda i: i[1])

        free_meetings_list = [[working_hours_start, working_hours_end]]

        for meeting in meetings_sorted_duration:
            free_meetings_list_temp = free_meetings_list
            for index_free, free_meeting in enumerate(free_meetings_list):
                meeting_starttime = self.convert_timezone(meeting[1])
                meeting_endtime = self.convert_timezone(meeting[2])
                free_starttime = free_meeting[0]
                free_endtime = free_meeting[1]

                if (free_starttime <= meeting_starttime) \
                        and (meeting_starttime <= free_endtime) \
                        and (free_starttime <= meeting_endtime) \
                        and (free_endtime <= meeting_endtime):
                    # case 1, meeting starts before freetime ends
                    free_meetings_list_temp[index_free][1] = meeting_starttime

                elif (meeting_starttime <= free_starttime) \
                        and (meeting_starttime <= free_endtime) \
                        and (free_starttime <= meeting_endtime) \
                        and (meeting_endtime <= free_endtime):
                    # case 2, meeting ends after freetime starts
                    free_meetings_list_temp[index_free][0] = meeting_endtime

                elif (free_starttime < meeting_starttime)  \
                        and (meeting_starttime < free_endtime) \
                        and (free_starttime < meeting_endtime) \
                        and (meeting_endtime < free_endtime):
                    # case 3, meeting lies between free time
                    free_meetings_list_temp[index_free][1] = meeting_starttime
                    free_meetings_list_temp.append([meeting_endtime, free_endtime])

                elif (meeting_starttime <= free_starttime) \
                        and (meeting_starttime <= free_endtime) \
                        and (free_starttime <= meeting_endtime) \
                        and (free_endtime <= meeting_endtime):
                    # case 4, freetime lies between meeting, delete
                    free_meetings_list_temp.remove(index_free)

            free_meetings_list = free_meetings_list_temp

        return free_meetings_list

    def convert_timezone(self, input_datetime: datetime) -> datetime:
        import pytz


        user_timezone = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
        output_datetime = pytz.utc.localize(input_datetime).astimezone(user_timezone)
        output_datetime = output_datetime.replace(tzinfo=None) #removes the +2:00 from utc
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
        
