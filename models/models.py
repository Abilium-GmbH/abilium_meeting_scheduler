# -*- coding: utf-8 -*-

from odoo import models, fields, api

class meeting_scheduler(models.Model):
    _name = 'meeting_scheduler'
    _description = 'meeting_scheduler'

    meetingTitle = fields.Char(string="Meeting Title")
    meetingStartDate = fields.Datetime(string="Start Date")
    meetingEndDate = fields.Datetime(string="End Date")
    meetingLocation = fields.Char(string="Location")
    meetingSubject = fields.Text(string="Subject")
    meetingDuration = fields.Char(string="Duration", compute="_calc_duration", store=True)
    meetingFrequency = fields.Selection([('0', 'Not repeating'), ('1', 'Weekly'), ('2', 'Biweekly')], store=True,
                                 string="Repeating", default='0')

    @api.depends('meetingStartDate', 'meetingEndDate')
    def _calc_duration(self):

        try:
            for record in self:
                record.meetingDuration = record.meetingEndDate - record.meetingStartDate
        except:
            record.meetingDuration = "Error"
