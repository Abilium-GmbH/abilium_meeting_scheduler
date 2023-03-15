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
    duration = fields.Char(string="Duration", compute="_calc_duration", store=True)
    frequency = fields.Selection([('0', 'Not repeating'), ('1', 'Weekly'), ('2', 'Biweekly')], store=True,
                                 string="Repeating", default='0')

    @api.depends('start_date', 'end_date')
    def _calc_duration(self):

        try:
            for record in self:
                record.duration = record.end_date - record.start_date
        except:
            record.duration = "Error"
