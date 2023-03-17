# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import models, fields, api
import datetime


class meeting_scheduler(models.Model):
    _name = 'meeting_scheduler'
    _description = 'meeting_scheduler'

    meeting_title = fields.Char(string="Meeting Title")
    meeting_start_date = fields.Datetime(string="Start Date", required="True")
    meeting_end_date = fields.Datetime(string="End Date", required="True")
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

        #created_records stores all the created records
        created_records = []

        #stores values given in the form for easier calculations and adjustments
        meeting_repetitions = data_list[0]['meeting_repetitions']
        meeting_frequency = data_list[0]['meeting_frequency']
        default_title = data_list[0]['meeting_title']

        #frequency 1 is weekly so add 7 days
        if meeting_frequency == '1':

            for x in range(meeting_repetitions):
                data_list[0]['meeting_title'] = default_title + " #" + str(x + 1)

                #datetime is stored as string, so we need to convert string to datetime object then add the days and then convert it back to a string
                data_list[0]['meeting_start_date'] = str(datetime.datetime.strptime(data_list[0]['meeting_start_date'],
                                                    "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=7))

                data_list[0]['meeting_end_date'] = str(datetime.datetime.strptime(data_list[0]['meeting_end_date'],
                                                    "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=7))

                created_records.append(super(meeting_scheduler, self).create(data_list))

        #frequency 2 is biweekly so add 14 days
        elif meeting_frequency == '2':

            for x in range(meeting_repetitions):
                data_list[0]['meeting_title'] = default_title + " #" + str(x + 1)
                data_list[0]['meeting_start_date'] = str(datetime.datetime.strptime(data_list[0]['meeting_start_date'],
                                                    "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=14))

                data_list[0]['meeting_end_date'] = str(datetime.datetime.strptime(data_list[0]['meeting_end_date'],
                                                    "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=14))

                created_records.append(super(meeting_scheduler, self).create(data_list))

        #else create normal record
        else:
            created_records.append(super(meeting_scheduler, self).create(data_list))

        #show the first meeting
        return created_records[0]
