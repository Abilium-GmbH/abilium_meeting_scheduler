# -*- coding: utf-8 -*-
from datetime import timedelta

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
    meeting_repetitions = fields.Integer(string="Number of repetitions")

    @api.depends('meeting_start_date', 'meeting_end_date')
    def _calc_duration(self):
        try:
            for record in self:
                record.meeting_duration = record.meeting_end_date - record.meeting_start_date
        except:
            record.meeting_duration = "Error"

    @api.model_create_multi
    def create(self, data_list):

        created_records = []

        data_list[0]['meeting_title'] = "stage 1"

        for x in range(5):
            data_list[0]['meeting_subject'] = "rec xx " + str(x)
            created_records.append(super(meeting_scheduler, self).create(data_list))

        return created_records[0]
