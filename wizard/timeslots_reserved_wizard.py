# -*- coding: utf-8 -*-

from odoo import models, fields, api
from typing import List
from datetime import datetime


class timeslots_reserved_wizard(models.TransientModel):
    _name = 'timeslots_reserved_wizard'
    _description = 'timeslots_reserved_wizard'

    def transit_button_confirm_meeting(self):
        return True



    def transit_button_reject_meeting(self):
        return True
