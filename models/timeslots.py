# -*- coding: utf-8 -*-
import datetime

import pytz

from odoo import models, fields, api
from typing import List
from datetime import datetime



class timeslots(models.Model):
    _name = 'timeslots'
    _description = 'timeslots'

    # meeting_title = fields.Char(string="Meeting Title", required=True)
    timeslots_start_date_str = fields.Char(string="Start Date (String)", required=True)
    timeslots_end_date_str = fields.Char(string="End Date (String)", required=True)
    timeslots_bookable_hours = fields.Char(string="timeslots_bookable_hours") #field for website dropdown selection
    timeslots_start_date_utc = fields.Datetime(string="Start Date (UTC)", required=True)
    timeslots_end_date_utc = fields.Datetime(string="End Date (UTC)", required=True)
    timeslots_groupmembers = fields.Char(string="Group Members (String)", required=True)

    # meeting_location = fields.Char(string="Location")
    # meeting_subject = fields.Text(string="Subject")
    # meeting_duration = fields.Char(string="Duration", compute="_calc_duration", store=True)
    # meeting_repetitions = fields.Integer(string="Number of repetitions", default=1)