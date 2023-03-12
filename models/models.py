# -*- coding: utf-8 -*-

from odoo import models, fields, api


class meeting_scheduler(models.Model):
    _name = 'meeting_scheduler'
    _description = 'meeting_scheduler'

    name = fields.Char(string="Your Name")
    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")
    location = fields.Char(string="Location")
    subject = fields.Text(string="Subject")
