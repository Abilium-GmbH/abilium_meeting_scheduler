# -*- coding: utf-8 -*-
import datetime

import pytz
import re

from odoo import models, fields, api
from typing import List
from datetime import datetime
from datetime import timedelta


class timeslots_confirmed(models.Model):
    _name = 'timeslots_confirmed'
    _description = 'timeslots_confirmed'

    meeting_title = fields.Char(string="Meeting Title", default="Meeting")
    firstname = fields.Char(string="First name", required=False)
    lastname = fields.Char(string="Last name", required=False)
    companyname = fields.Char(string="Company", required=False)
    email = fields.Char(string="E-Mail", required=False)
    timeslots_start_date = fields.Datetime(string="Start Date", required=False)
    timeslots_end_date = fields.Datetime(string="End Date", required=False)
    timeslots_id = fields.Integer(string="Foreign Key timeslots")
    timeslots_reserved_location = fields.Char(string="Location")
    timeslots_reserved_meeting_subject = fields.Text(string="Subject")
    timeslots_reserved_meeting_duration = fields.Char(string="Duration")
    timeslots_confirmed_token = fields.Char(string="Token")
    timeslots_confirmed_link = fields.Char(string="Link")
    timeslots_confirmed_calendar_event_id = fields.Integer(string="Foreign Key calendar_event")
    timeslots_reserved_participants = fields.Char(string="Participants")
    corresponding_calendar_event = fields.Many2one('calendar.event',
                                                   string="Corresponding Calendar Event",
                                                   ondelete="cascade", readonly="True")
    bool_deleted_by_guest = fields.Boolean(string="Deleted by Guest", default=False)

    def button_cancel_meeting(self, timeslots_confirmed_object):
        """
        this function deletes the timeslots_confirmed entry and the corresponding calendar_event,
        and sends an email to the guest about the cancellation
        :param timeslots_confirmed_object:
        :return:
        """
        timeslots_confirmed_object.bool_deleted_by_guest = True
        body_html = "This E-Mail confirms that you have cancelled the following Meeting: </br>" \
                    + "<h1>" + str(timeslots_confirmed_object.meeting_title) + "</h1>" \
                    + "<p>Starting on the <b>" + str(timeslots_confirmed_object.timeslots_start_date) + "</b></br>" \
                    + "participants: " + str(timeslots_confirmed_object.firstname) + " " \
                    + str(timeslots_confirmed_object.lastname) + ", " \
                    + str(timeslots_confirmed_object.companyname) + "</br>"
        if (str(timeslots_confirmed_object.timeslots_reserved_meeting_subject) != "False"):
            body_html = body_html + "description: " + str(timeslots_confirmed_object.timeslots_reserved_meeting_subject)
        body_html = body_html + " </p>"
        self.env['timeslots_reserved'].send_mail_to_address(
            "CANCELLED " + str(timeslots_confirmed_object.meeting_title), body_html,
            str(timeslots_confirmed_object.email))
        self.recreate_meetings(timeslots_confirmed_object)
        # self.env['calendar.event'].browse(timeslots_confirmed_object.timeslots_confirmed_calendar_event_id).unlink()
        timeslots_confirmed_object.unlink()

    def recreate_meetings(self, timeslots_confirmed_object):
        timeslots_confirmed_user_ids = []
        for i in re.split('\[|,| |\]', timeslots_confirmed_object.timeslots_reserved_participants):
            if i.isnumeric():
                timeslots_confirmed_user_ids.append(int(i))
                meeting_before_found_id = self.env['meeting_scheduler'].search(['&',
                                                                                ('meeting_end_date', '=',
                                                                                 timeslots_confirmed_object.timeslots_start_date),
                                                                                ('create_uid', '=', int(i))])
                meeting_after_found_id = self.env['meeting_scheduler'].search(['&',
                                                                               ('meeting_start_date', '=',
                                                                                timeslots_confirmed_object.timeslots_end_date),
                                                                               ('create_uid', '=', int(i))])
                if (meeting_before_found_id.id != False):
                    if (meeting_after_found_id.id != False):
                        self.env['meeting_scheduler'].with_env(self.env(user=int(i))).create([{
                            'meeting_title': self.env['ir.config_parameter'].sudo().get_param(
                                'meeting_scheduler.meeting_title_default'),  # use the values from the settings
                            'meeting_location': False,
                            'meeting_start_date': meeting_before_found_id.meeting_start_date,
                            'meeting_end_date': meeting_after_found_id.meeting_end_date,
                            'meeting_repetitions': 1,
                            'meeting_frequency': 0,
                            'meeting_privacy': 'public',
                            'meeting_show_as': 'free',
                            'meeting_subject': False
                        }])
                        meeting_before_found_id.unlink()
                        meeting_after_found_id.unlink()

                    else:
                        self.env['meeting_scheduler'].with_env(self.env(user=int(i))).create([{
                            'meeting_title': self.env['ir.config_parameter'].sudo().get_param(
                                'meeting_scheduler.meeting_title_default'),  # use the values from the settings
                            'meeting_location': False,
                            'meeting_start_date': meeting_before_found_id.meeting_start_date,
                            'meeting_end_date': timeslots_confirmed_object.timeslots_end_date,
                            'meeting_repetitions': 1,
                            'meeting_frequency': 0,
                            'meeting_privacy': 'public',
                            'meeting_show_as': 'free',
                            'meeting_subject': False
                        }])
                        meeting_before_found_id.unlink()

                if (meeting_after_found_id.id != False) & (not meeting_before_found_id.id):
                    self.env['meeting_scheduler'].with_env(self.env(user=int(i))).create([{
                        'meeting_title': self.env['ir.config_parameter'].sudo().get_param(
                            'meeting_scheduler.meeting_title_default'),  # use the values from the settings
                        'meeting_location': False,
                        'meeting_start_date': timeslots_confirmed_object.timeslots_start_date,
                        'meeting_end_date': meeting_after_found_id.meeting_end_date,
                        'meeting_repetitions': 1,
                        'meeting_frequency': 0,
                        'meeting_privacy': 'public',
                        'meeting_show_as': 'free',
                        'meeting_subject': False
                    }])
                    meeting_after_found_id.unlink()

                if (not meeting_before_found_id.id) and (not meeting_after_found_id.id):
                    # for the case that the meeting has no meetings directly before or after
                    self.env['meeting_scheduler'].with_env(self.env(user=int(i))).create([{
                        'meeting_title': self.env['ir.config_parameter'].sudo().get_param(
                            'meeting_scheduler.meeting_title_default'),  # use the values from the settings
                        'meeting_location': False,
                        'meeting_start_date': timeslots_confirmed_object.timeslots_start_date,
                        'meeting_end_date': timeslots_confirmed_object.timeslots_end_date,
                        'meeting_repetitions': 1,
                        'meeting_frequency': 0,
                        'meeting_privacy': 'public',
                        'meeting_show_as': 'free',
                        'meeting_subject': False
                    }])
        # upon confirming a meeting, this section generates new bookable timeslots for that day
        self.env['timeslots_reserved'].generate_new_bookable_timeslots(timeslots_confirmed_object.timeslots_start_date,
                                                                       timeslots_confirmed_user_ids)
        return True

    def unlink(self):
        self.recreate_meetings(self)
        if(not self.bool_deleted_by_guest):
            body_html = "We sadly have to inform you, that the following Meeting was cancelled: </br>" \
                        + "<h1>" + str(self.meeting_title) + "</h1>" \
                        + "<p>Starting on the <b>" + str(self.timeslots_start_date) + "</b></br>" \
                        + "participants: " + str(self.firstname) + " " \
                        + str(self.lastname) + ", " \
                        + str(self.companyname) + "</br>"

            if str(self.timeslots_reserved_meeting_subject) != "False":
                body_html = body_html + "description: " + str(self.timeslots_reserved_meeting_subject)

            body_html = body_html + " </p>"
            domain = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            link = domain + '/meeting_scheduler/guest_view/'
            link = "\"" + link + "\""
            body_html = body_html + "<p>Follow this link to schedule a meeting: </br> <a href=" + link + ">Meeting scheduler</a>   </p>"
            self.env['timeslots_reserved'].send_mail_to_address(
                "CANCELLATION " + str(self.meeting_title), body_html,
                str(self.email))
        self.corresponding_calendar_event.unlink()
        return True
