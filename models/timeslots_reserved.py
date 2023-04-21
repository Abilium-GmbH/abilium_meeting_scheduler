# -*- coding: utf-8 -*-
import datetime

import pytz

from odoo import models, fields, api
from typing import List
from datetime import datetime



class timeslots_reserved(models.Model):
    _name = 'timeslots_reserved'
    _description = 'timeslots_reserved'

    meeting_title = fields.Char(string="Meeting Title", required=False)
    firstname = fields.Char(string="firstname", required=False)
    lastname = fields.Char(string="lastname", required=False)
    companyname = fields.Char(string="companyname", required=False)
    email = fields.Char(string="email", required=False)
    timeslots_start_date = fields.Datetime(string="Start Date", required=False)
    timeslots_end_date = fields.Datetime(string="End Date", required=False)
    # meeting_location = fields.Char(string="Location")
    # meeting_subject = fields.Text(string="Subject")
    # meeting_duration = fields.Char(string="Duration", compute="_calc_duration", store=True)
    # meeting_repetitions = fields.Integer(string="Number of repetitions", default=1)