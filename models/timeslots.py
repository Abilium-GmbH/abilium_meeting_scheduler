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
    timeslots_start_date = fields.Char(string="Start Date", required=True)
    timeslots_end_date = fields.Char(string="End Date", required=True)
    timeslots_bookable_hours = fields.Char(string="timeslots_bookable_hours")
    timeslots_duration_hours = fields.Char(string="timeslots_duration_hours")
    # meeting_location = fields.Char(string="Location")
    # meeting_subject = fields.Text(string="Subject")
    # meeting_duration = fields.Char(string="Duration", compute="_calc_duration", store=True)
    # meeting_repetitions = fields.Integer(string="Number of repetitions", default=1)