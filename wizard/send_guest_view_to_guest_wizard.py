# -*- coding: utf-8 -*-

from odoo import models, fields, api
from typing import List
from datetime import datetime


class send_guest_view_to_guest_wizard(models.TransientModel):
    _name = 'send_guest_view_to_guest_wizard'
    _description = 'send_guest_view_to_guest_wizard'

    mail_address = fields.Char(string="Mail Address")

    def button_send_mail(self):
        domain = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        link = domain + '/meeting_scheduler/guest_view/'
        link = "\"" + link + "\""
        body_html = "<p>Follow this link to schedule a meeting: </br> <a href=" + link + ">Meeting scheduler</a>   </p>"
        self.env['timeslots_reserved'].send_mail_to_address(
            "INVITATION ", body_html,
            str(self.mail_address))

        return True
