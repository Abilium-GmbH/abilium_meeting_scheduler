# -*- coding: utf-8 -*-

from odoo import models, fields, api


class meeting_scheduler(models.Model):
    _name = 'meeting_scheduler'
    _description = 'meeting_scheduler'

    name = fields.Char(string="Name")
    value = fields.Integer(string="value")
    value2 = fields.Float(string="value2", compute="_value_pc", store=True)
    description = fields.Text()

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100
