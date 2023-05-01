# -*- coding: utf-8 -*-
import datetime

import pytz
import re

from odoo import models, fields, api
from typing import List
from datetime import datetime
from datetime import timedelta


class timeslots_reserved(models.Model):
    _name = 'timeslots_reserved'
    _description = 'timeslots_reserved'

    meeting_title = fields.Char(string="Meeting Title", default="Meeting")
    firstname = fields.Char(string="firstname", required=False)
    lastname = fields.Char(string="lastname", required=False)
    companyname = fields.Char(string="companyname", required=False)
    email = fields.Char(string="email", required=False)
    timeslots_start_date = fields.Datetime(string="Start Date", required=False)
    timeslots_end_date = fields.Datetime(string="End Date", required=False)
    timeslots_id = fields.Integer(string="Foreign Key timeslots")
    timeslots_reserved_location = fields.Char(string="Location")
    timeslots_reserved_meeting_subject = fields.Text(string="Subject")
    timeslots_reserved_meeting_duration = fields.Char(string="Duration")

    def open_confirm_form(self):
        """
        needed for the timeslots_reserved_wizard
        :return:
        """

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'timeslots_reserved_wizard',  # name of respective model,
            # 'views': [('group_scheduler_timeform', 'form')],  # view id and type
            'view_id': self.env.ref('meeting_scheduler.timeslots_reserved_confirmform').id,  # view id
            'target': 'new',
            # 'context': context,
        }

    # might not be used
    # def get_user_ids_from_timeslot_id(self, timeslot_id):
    #     """
    #     returns a list with the user_ids from the selected meeting timeslot
    #     :param timeslot_id: an int (or string ?) is accepted, representing the id of the bookable timeslot entry
    #     :return: a list with the user_ids from the selected meeting [user_id_1, user_id_2]
    #     """
    #     timeslots_original = self.env['timeslots'].browse(int(timeslot_id))
    #     output_user_ids = []
    #     for i in re.split('\[|,| |\]', timeslots_original.timeslots_groupmembers):
    #         if i.isnumeric():
    #             output_user_ids.append(int(i))
    #     return output_user_ids

    def get_partner_ids_from_timeslot_id(self, timeslot_id):
        """
        returns a list with the partner_ids from the selected meeting timeslot
        :param timeslot_id: an int (or string ?) is accepted, representing the id of the bookable timeslot entry
        :return: a list with the partner_ids from the selected meeting [partner_id_1, partner_id_2]
        """
        timeslots_original = self.env['timeslots'].browse(int(timeslot_id))
        output_partner_ids = []
        for i in re.split('\[|,| |\]', timeslots_original.timeslots_groupmembers):
            if i.isnumeric():
                selected_user = self.env['res.users'].search([('id', '=', int(i))])
                output_partner_ids.append(selected_user['partner_id'].id)

        return output_partner_ids




    def button_confirm_meeting(self, ourloaction):
        self.env['print_table'].create({'show_stuff': str(ourloaction)})
        timeslots_minimal_rest_time = timedelta(minutes=15)
        selected_timeslot_reserved = self.env.context.get('active_ids', [])
        timeslot_selected_records = self.env['timeslots_reserved'].browse(selected_timeslot_reserved)
        timeslot_selected_record_id = timeslot_selected_records.timeslots_id
        timeslots_original = self.env['timeslots'].browse(timeslot_selected_record_id)
        # self.env['print_table'].create({'show_stuff': timeslots_original.timeslots_groupmembers.split()})


        partner_id_list = []
        for i in re.split('\[|,| |\]', timeslots_original.timeslots_groupmembers):
            if i.isnumeric():
                temp_meeting_scheduler = self.env['meeting_scheduler'].search([('create_uid', '=', int(i)),
                                                             ('meeting_start_date', '<=', timeslot_selected_records.timeslots_start_date),
                                                             ('meeting_end_date', '>=', timeslot_selected_records.timeslots_end_date),
                                                             ('meeting_end_date', '>', timeslot_selected_records.timeslots_start_date)])

                temp_calendar_event = self.env['calendar.event'].search([('create_uid', '=', int(i)),
                                                                         ('start', '<=',
                                                                          timeslot_selected_records.timeslots_start_date),
                                                                         ('stop', '>=',
                                                                          timeslot_selected_records.timeslots_end_date),
                                                                         ('stop', '>',
                                                                          timeslot_selected_records.timeslots_start_date)])

                # https://stackoverflow.com/questions/35599788/adding-partners-to-calendar-in-odoo
                # (0, 0, { values }) link to a new record that needs to be created with the given values dictionary
                # (1, ID, { values }) update the linked record with id = ID (write values on it)
                # (2, ID) remove and delete the linked record with id = ID (calls unlink on ID, that will delete the object completely, and the link to #it as well)
                # (3, ID) cut the link to the linked record with id = ID (delete the relationship between the two objects but does not delete the target #object itself)
                # (4, ID) link to existing record with id = ID (adds a relationship)
                # (5) unlink all (like using (3,ID) for all linked records)
                # (6, 0, [IDs]) replace the list of linked IDs (like using (5) then (4,ID) for each ID in the list of IDs)
                selected_user = self.env['res.users'].search([('id', '=', int(i))])
                partner_id_list.append(selected_user['partner_id'].id)
                if((timeslot_selected_records.timeslots_start_date - temp_meeting_scheduler.meeting_start_date) > timeslots_minimal_rest_time):
                    self.env['meeting_scheduler'].with_env(self.env(user=int(i))).create([{
                        'meeting_title': 'meetingBookable',
                        'meeting_location': False,
                        'meeting_start_date': temp_meeting_scheduler.meeting_start_date,
                        'meeting_end_date': timeslot_selected_records.timeslots_start_date,
                        'meeting_repetitions': 1,
                        'meeting_frequency': 0,
                        'meeting_privacy': 'public',
                        'meeting_show_as': 'free',
                        'meeting_subject': False
                    }])
                if((temp_meeting_scheduler.meeting_end_date - timeslot_selected_records.timeslots_end_date) > timeslots_minimal_rest_time):

                    self.env['meeting_scheduler'].with_env(self.env(user=int(i))).create([{
                        'meeting_title': 'meetingBookable',
                        'meeting_location': False,
                        'meeting_start_date': timeslot_selected_records.timeslots_end_date,
                        'meeting_end_date': temp_meeting_scheduler.meeting_end_date,
                        'meeting_repetitions': 1,
                        'meeting_frequency': 0,
                        'meeting_privacy': 'public',
                        'meeting_show_as': 'free',
                        'meeting_subject': False
                    }])

                temp_calendar_event.unlink()

        self.env['calendar.event'].create({
                                              'name': "Booked meeting with" + timeslot_selected_records.firstname + " " + timeslot_selected_records.lastname,
                                              'privacy': 'public',
                                              'show_as': 'busy',
                                              'start': timeslot_selected_records.timeslots_start_date,
                                              'stop': timeslot_selected_records.timeslots_end_date,
                                              'partner_ids': [[6, 0, partner_id_list]]})

        timeslots_original.unlink()
        timeslot_selected_records.unlink()

        return True

    def button_reject_meeting(self):
        return True
