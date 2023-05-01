# -*- coding: utf-8 -*-

from odoo import models, fields, api
from typing import List
from datetime import datetime


class timeslots_reserved_wizard(models.TransientModel):
    _name = 'timeslots_reserved_wizard'
    _description = 'timeslots_reserved_wizard'

    dummy = fields.Char(string="dummy ist dumm")
    wiz_meeting_title = fields.Char(string="Meeting title", readonly=True, compute='compute_get_selected_field')
    wiz_firstname = fields.Char(string="First name", readonly=True)
    wiz_lastname = fields.Char(string="Last name", readonly=True)
    wiz_companyname = fields.Char(string="Company", readonly=True)
    wiz_email = fields.Char(string="E-Mail", readonly=True)
    wiz_timeslots_start_date = fields.Datetime(string="Start Date", readonly=True)
    wiz_timeslots_end_date = fields.Datetime(string="End Date", readonly=True)
    wiz_timeslots_reserved_location = fields.Char(string="Location", required=True)
    wiz_timeslots_reserved_meeting_subject = fields.Text(string="Subject", readonly=True)
    wiz_timeslots_reserved_meeting_duration = fields.Char(string="Duration", readonly=True)




    # firstname2 = fields.Char(related='timeslots_reserverd.firstname')

    # selected_timeslot_reserved = self.env.context.get('active_ids', [])
    # timeslot_selected_records = self.env['timeslots_reserved'].browse(selected_timeslot_reserved)

    @api.depends('dummy')
    def compute_get_selected_field(self):

        selected_timeslot_reserved = self.env.context.get('active_ids', [])
        timeslot_selected_records = self.env['timeslots_reserved'].browse(selected_timeslot_reserved)
        # records.firstname = timeslot_selected_records.firstname

        for record in self:
            record.wiz_meeting_title = timeslot_selected_records.meeting_title
            record.wiz_firstname = timeslot_selected_records.firstname
            record.wiz_lastname = timeslot_selected_records.lastname
            record.wiz_companyname = timeslot_selected_records.companyname
            record.wiz_email = timeslot_selected_records.email
            record.wiz_timeslots_start_date = timeslot_selected_records.timeslots_start_date
            # record.wiz_timeslots_reserved_location = timeslot_selected_records.timeslots_reserved_location
            record.wiz_timeslots_reserved_meeting_subject = timeslot_selected_records.timeslots_reserved_meeting_subject
            record.wiz_timeslots_reserved_meeting_duration = timeslot_selected_records.timeslots_reserved_meeting_duration

    def transit_button_confirm_meeting(self):
        for record in self:
            self.env['print_table'].create({'show_stuff': str(record.wiz_timeslots_reserved_location)})
            return self.env['timeslots_reserved'].button_confirm_meeting(record.wiz_timeslots_reserved_location)

    def transit_button_reject_meeting(self):
        return True

    def button_mailtester(self):

        mail_obj = self.env['mail.mail']
        body_html = "<p>message</p>"
        mail = mail_obj.create({
            'subject': "testtstse",
            'body_html': body_html,
            'email_to': ("bla"),
        })
        mail.send()

    def do_teh_chatter(self):
        body = "My Message!"
        partner_id = 3 #odoobot 2
        notification_ids = []
        notification_ids.append((0,0, {
            'res_partner_id': partner_id,
            'notification_type': 'inbox'}))

        message_vals = {
            'body': body,
            'subject': "run",
            'author_id': self.env.user.partner_id.id,
            'model': self._name,
            'res_id': self.id,
            # 'partner_ids': [(4, partner_id)]
            'partner_ids': [(4, partner_id)],
            # 'notification': True,
            'message_type': 'notification',
            'notification_ids': notification_ids,
            # 'type': 'notification',
            # 'subtype_id': self.env.ref('mail.mt_notification').id
        }
        self.env['mail.message'].create(message_vals)

        # return {
        #     'effect': {
        #         'fadeout': 'slow',
        #         'message': 'Hellooo',
        #         'type': 'rainbow_man',
        #     }
        # }
