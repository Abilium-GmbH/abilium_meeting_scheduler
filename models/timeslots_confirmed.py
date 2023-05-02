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
    timeslots_confirmed_token = fields.Char(string="Token")


