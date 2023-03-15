# -*- coding: utf-8 -*-

from odoo import models, fields, api


class meeting_scheduler(models.Model):
    _name = 'meeting_scheduler'
    _description = 'meeting_scheduler'

    meeting_title = fields.Char(string="Meeting Title")
    meeting_start_date = fields.Datetime(string="Start Date")
    meeting_end_date = fields.Datetime(string="End Date")
    meeting_location = fields.Char(string="Location")
    meeting_subject = fields.Text(string="Subject")
    meeting_duration = fields.Char(string="Duration", compute="_calc_duration", store=True)
    meeting_frequency = fields.Selection([('0', 'Not repeating'), ('1', 'Weekly'), ('2', 'Biweekly')], store=True,
                                 string="Repeating", default='0')

    @api.depends('meeting_start_date', 'meeting_end_date')
    def _calc_duration(self):

        try:
            for record in self:
                record.meeting_duration = record.meeting_end_date - record.meeting_start_date
        except:
            record.meeting_duration = "Error"
