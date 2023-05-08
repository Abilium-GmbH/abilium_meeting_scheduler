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
    wiz_timeslots_reserved_location = fields.Char(string="Location")
    wiz_timeslots_reserved_meeting_subject = fields.Text(string="Subject", readonly=True)
    wiz_timeslots_reserved_meeting_duration = fields.Char(string="Duration", readonly=True)

    @api.depends('dummy') #TODO find a solution without the dummy
    def compute_get_selected_field(self):
        """
        loads the actual values from the selected timeslots_reserved record in the wizard
        :return:
        """
        selected_timeslot_reserved = self.env.context.get('active_ids', [])
        timeslot_selected_records = self.env['timeslots_reserved'].browse(selected_timeslot_reserved)
        for record in self:
            record.wiz_meeting_title = timeslot_selected_records.meeting_title
            record.wiz_firstname = timeslot_selected_records.firstname
            record.wiz_lastname = timeslot_selected_records.lastname
            record.wiz_companyname = timeslot_selected_records.companyname
            record.wiz_email = timeslot_selected_records.email
            record.wiz_timeslots_start_date = timeslot_selected_records.timeslots_start_date
            # record.wiz_timeslots_reserved_location = timeslot_selected_records.timeslots_reserved_location #do not load location, else it will be overwritten
            record.wiz_timeslots_reserved_meeting_subject = timeslot_selected_records.timeslots_reserved_meeting_subject
            record.wiz_timeslots_reserved_meeting_duration = timeslot_selected_records.timeslots_reserved_meeting_duration

    def transit_button_confirm_meeting(self):
        for record in self:
            if (record.wiz_timeslots_reserved_location != False):
                return self.env['timeslots_reserved'].button_confirm_meeting(record.wiz_timeslots_reserved_location)
            else:
                return {
                    'type': 'ir.actions.client',
                     'tag': 'display_notification',
                    'params': {
                        'title': 'Error',
                        'type': 'danger',
                        'message': 'Please enter a location',
                        'sticky': False,
                        }}


    def transit_button_reject_meeting(self):
        return self.env['timeslots_reserved'].button_reject_meeting()

    def button_mailtester(self):
        """
        sends a mail with meeting description to the guest
        :return:
        """

        domain = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Hellooo Roger',
                'type': 'rainbow_man',
            }
        }

    def send_internal_notification(self, subject, message, partner_ids, modelname):
        """
        Creates an internal message in the Discuss module
        :param subject: message subject, string
        :param message: message content, string
        :param partner_ids: list of partner_ids who are the recipents [partner_id_1, partner_id2]
        :param modelname: the modelname of the sending model, for example request.env['timeslots_reserved']._name
        :return:
        """
        # partner_id = 3 #odoobot 2
        for partner_id in partner_ids:
            notification_ids = []
            notification_ids.append((0, 0, {
                'res_partner_id': partner_id,
                'notification_type': 'inbox'}))

            message_vals = {
                'body': message,
                'subject': subject,
                'author_id': self.env.user.partner_id.id,
                # 'model': self._name,
                'model': modelname,
                'res_id': self.id,
                'partner_ids': [(4, partner_id)],
                'message_type': 'notification',
                'notification_ids': notification_ids,
            }
            self.env['mail.message'].create(message_vals)


