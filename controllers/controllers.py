# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import route, request
from datetime import datetime
from datetime import timedelta
import pytz

class MeetingScheduler(http.Controller):

    @route('/meeting_scheduler/guest_view/', auth='public', website=True)
    def index(self, **kw):
        records = request.env['timeslots'].sudo().search([])
        response = request.render("meeting_scheduler.guest_view_loop", {'value': records,
                                                                        'checkboxValue': True})
        inputs_contact = []
        inputs_meeting = []
        if((kw.get('firstname') is not None) and (kw.get('firstname') != '')):
            inputs_contact.append(kw.get('firstname'))
        if((kw.get('lastname') is not None) and (kw.get('lastname') != '')):
            inputs_contact.append(kw.get('lastname'))
        if((kw.get('companyname') is not None) and (kw.get('companyname') != '')):
            inputs_contact.append(kw.get('companyname'))
        if((kw.get('email') is not None) and (kw.get('email') != '')):
            inputs_contact.append(kw.get('email'))
        if((kw.get('meetingtitle') is not None) and (kw.get('meetingtitle') != '')):
            inputs_contact.append(kw.get('meetingtitle'))
        if((kw.get('id') is not None) and (kw.get('id') != '')
            and(kw.get('sel_start_h') is not None) and (kw.get('sel_start_h') != '')
            and (kw.get('sel_start_min') is not None) and (kw.get('sel_start_min') != '')
           
           #and (kw.get('sel_end_h') is not None) and (kw.get('sel_end_h') != '')
           #and (kw.get('sel_end_min') is not None) and (kw.get('sel_end_min') != '')):         
            and (kw.get('sel_duration_h') is not None) and (kw.get('sel_duration_h') != '')
            and (kw.get('sel_duration_min') is not None) and (kw.get('sel_duration_min') != '')):
          
            temp_id = kw.get('id')
            
            #temp_start = (request.env['timeslots'].search([('id', '=', temp_id)])['timeslots_start_date_str'])
            #temp_start = datetime.strptime(temp_start[0:10], '%Y-%m-%d')
            #temp_start = temp_start.replace(hour = int(kw.get('sel_start_h')), minute= int(kw.get('sel_start_min')))
            temp_start_zurich = (request.env['timeslots'].search([('id', '=', temp_id)])['timeslots_start_date_str'])
            temp_start_zurich = datetime.strptime(temp_start_zurich[0:16], '%Y-%m-%d %H:%M')
            temp_start_zurich = temp_start_zurich.replace(hour = int(kw.get('sel_start_h')) - temp_start_zurich.hour , minute= int(kw.get('sel_start_min')))
            temp_start_zurich_utc = (request.env['timeslots'].search([('id', '=', temp_id)])['timeslots_start_date_utc'])
            temp_start_zurich_utc = temp_start_zurich_utc.replace(hour = temp_start_zurich_utc.hour + temp_start_zurich.hour, minute = temp_start_zurich.minute)

            #inputs_meeting.append(temp_start)
            inputs_meeting.append(temp_start_zurich_utc)

            temp_end = (request.env['timeslots'].search([('id', '=', temp_id)])['timeslots_start_date_str'])
            temp_end = datetime.strptime(temp_end[0:10], '%Y-%m-%d')
            #temp_end = temp_end.replace(hour = int(kw.get('sel_end_h')), minute= int(kw.get('sel_end_min')))
            
            if ((inputs_meeting[0].minute + int(kw.get('sel_duration_min')))<60):
                temp_end = temp_end.replace(hour = inputs_meeting[0].hour + int(kw.get('sel_duration_h')),
                                            minute= inputs_meeting[0].minute + int(kw.get('sel_duration_min')))
                inputs_meeting.append(temp_end)
            if ((inputs_meeting[0].minute + int(kw.get('sel_duration_min')))>=60):
                temp_end = temp_end.replace(hour=inputs_meeting[0].hour + int(kw.get('sel_duration_h')) + 1,
                                            minute=(inputs_meeting[0].minute + int(kw.get('sel_duration_min')))-60)
                inputs_meeting.append(temp_end)
                
            inputs_meeting.append(temp_id)

        if(len(inputs_contact) == 5) and (len(inputs_meeting) == 3):
            duration = inputs_meeting[1] -inputs_meeting[0]
            # create a new timeslots reserved element
            reservation = request.env['timeslots_reserved'].create({'firstname': inputs_contact[0],
                                                      'lastname': inputs_contact[1],
                                                      'companyname': inputs_contact[2],
                                                      'email': inputs_contact[3],
                                                      'meeting_title': inputs_contact[4],
                                                      'timeslots_start_date': inputs_meeting[0],
                                                      'timeslots_end_date': inputs_meeting[1],
                                                      'timeslots_id': inputs_meeting[2],
                                                      'timeslots_reserved_meeting_duration': duration})
            # create an activity
            list_guest_ids = request.env['timeslots_reserved'].get_user_ids_from_timeslot_id(inputs_meeting[2])
            for user in list_guest_ids:
                request.env['mail.activity'].create({
                    'display_name': 'NEW timeslot reservation',
                    'summary': 'please confirm or reject the reservation',
                    'date_deadline': datetime.now(),
                    'user_id': user,
                    'res_id': reservation.id,
                    'res_model_id': request.env['ir.model']._get(request.env['timeslots_reserved']._name).id,
                    'activity_type_id': request.env.ref('mail.mail_activity_data_todo').id
                })
            # create a confirmation mail
            list_partner_ids = request.env['timeslots_reserved'].get_partner_ids_from_timeslot_id(inputs_meeting[2])
            request.env['timeslots_reserved_wizard'].send_internal_notification("NEW timeslot reservation",
                                                                                "please confirm or reject the reservation",
                                                                                list_partner_ids,
                                                                                request.env['timeslots_reserved']._name) # TODO add the messages to variables in a settings model           
            # show a confirmation for the received reservation
            response = request.render("meeting_scheduler.guest_view_confirm", {'value': reservation,
                                                                               'converted_start_date': str(request.env['group_scheduler'].convert_timezone(reservation.timeslots_start_date))})
        if((len(inputs_contact) != 5) or (len(inputs_meeting) != 3)) and (kw.get('id') is not None) and (kw.get('id') != ''):
            response = request.render("meeting_scheduler.guest_view_error", {})
        return response

    @route('/meeting_scheduler/scheduled_meeting/', auth='public', website=True)
    def token_check(self, **kw):
        hours_int = int(request.env['ir.config_parameter'].sudo().get_param('meeting_scheduler.locktime_hours_default'))
        locktime = timedelta(hours=hours_int)
        response = request.render("meeting_scheduler.token_entry", {})
        selected_meeting = request.env['timeslots_confirmed'].search([('timeslots_confirmed_token', '=', kw.get('token'))])
        if (selected_meeting.id != False):
            if((selected_meeting.timeslots_start_date - datetime.now()) < locktime):
                response = request.render("meeting_scheduler.token_locktime", {'value': selected_meeting,
                                                                               'locktime': str(locktime.days)+" days "+str(locktime.seconds//3600)+" hours"})
            else:
                response = request.render("meeting_scheduler.token_ok", {'value': selected_meeting})
        if(kw.get('token') == selected_meeting['timeslots_confirmed_token']) and (kw.get('id') == 'cancel'):
            request.env['timeslots_confirmed'].button_cancel_meeting(selected_meeting)
            response = request.render("meeting_scheduler.token_deleted", {})

        return response
