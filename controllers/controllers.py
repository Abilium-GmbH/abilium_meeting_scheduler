# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import route, request
from datetime import datetime
from datetime import timedelta

class MeetingScheduler(http.Controller):
    # @http.route('/meeting_scheduler/meeting_scheduler/', auth='public')
    # def index(self, **kw):
    #     return "Hello, world"


    @route('/meeting_scheduler/guest_view/', auth='public', website=True)
    def index(self, **kw):
        records = request.env['timeslots'].sudo().search([])
        # records = request.env['meeting_scheduler'].sudo().search([])
        # request.env['print_table'].create({'show_stuff': records})
        response = request.render("meeting_scheduler.guest_view_loop", {'value': records})
        inputs_contact = []
        inputs_meeting = []
        if((kw.get('firstname') is not None) and (kw.get('firstname') != '')):
            # request.env['print_table'].create({'show_stuff': firstname})
            inputs_contact.append(kw.get('firstname'))
        if((kw.get('lastname') is not None) and (kw.get('lastname') != '')):
            inputs_contact.append(kw.get('lastname'))
        if((kw.get('companyname') is not None) and (kw.get('companyname') != '')):
            inputs_contact.append(kw.get('companyname'))
        if((kw.get('email') is not None) and (kw.get('email') != '')):
            inputs_contact.append(kw.get('email'))
        if((kw.get('id') is not None) and (kw.get('id') != '')
            and(kw.get('sel_start_h') is not None) and (kw.get('sel_start_h') != '')
            and (kw.get('sel_start_min') is not None) and (kw.get('sel_start_min') != '')
            and (kw.get('sel_end_h') is not None) and (kw.get('sel_end_h') != '')
            and (kw.get('sel_end_min') is not None) and (kw.get('sel_end_min') != '')):
            temp_id = kw.get('id')
            # self.env['timeslots'].get_id(temp_id)
            temp_start = (request.env['timeslots'].search([('id', '=', temp_id)])['timeslots_start_date_str'])
            temp_start = datetime.strptime(temp_start[0:10], '%Y-%m-%d')
            temp_start = temp_start.replace(hour = int(kw.get('sel_start_h')), minute= int(kw.get('sel_start_min')))
            #
            # import pytz
            # user_timezone = pytz.timezone(request.env.context.get('tz') or request.env.user.tz)
            # # temp_start = user_timezone.localize(temp_start, is_dst=None)
            #
            #
            # temp_start = user_timezone.normalize(temp_start)
            # temp_start = temp_start.astimezone(pytz.utc)
            inputs_meeting.append(temp_start)

            temp_end = (request.env['timeslots'].search([('id', '=', temp_id)])['timeslots_start_date_str'])
            temp_end = datetime.strptime(temp_end[0:10], '%Y-%m-%d')
            temp_end = temp_end.replace(hour = int(kw.get('sel_end_h')), minute= int(kw.get('sel_end_min')))
            inputs_meeting.append(temp_end)
            inputs_meeting.append(temp_id)

        if(len(inputs_contact) == 4) and (len(inputs_meeting) == 3):
            request.env['timeslots_reserved'].create({'firstname': inputs_contact[0],
                                                      'lastname': inputs_contact[1],
                                                      'companyname': inputs_contact[2],
                                                      'email': inputs_contact[3],
                                                      'timeslots_start_date': inputs_meeting[0],
                                                      'timeslots_end_date': inputs_meeting[1],
                                                      'timeslots_id': inputs_meeting[2]})
            list_partner_ids = request.env['timeslots_reserved'].get_partner_ids_from_timeslot_id(inputs_meeting[2])
            request.env['timeslots_reserved_wizard'].send_internal_notification("NEW timeslot reservation",
                                                                                "please confirm or reject the reservation",
                                                                                list_partner_ids,
                                                                                request.env['timeslots_reserved']._name) # TODO add the messages to variables in a settings model

        return response

    # /meeting_scheduler/scheduled_meeting/?token=toki
    # /meeting_scheduler/scheduled_meeting/?token=23bce225f8dad88de2f89430f6f1dfc0
    @route('/meeting_scheduler/scheduled_meeting/', auth='public', website=True)
    def token_check(self, **kw):
        locktime = timedelta(hours=23)
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

    # @http.route('/meeting_scheduler/meeting_scheduler/objects/', auth='public')
    # def list(self, **kw):
    #     return http.request.render('meeting_scheduler.listing', {
    #         'root': '/meeting_scheduler/meeting_scheduler',
    #         'objects': http.request.env['meeting_scheduler'].search([]),
    #     })
    #
    # @http.route('/meeting_scheduler/meeting_scheduler/objects/<model("meeting_scheduler"):obj>/', auth='public')
    # def object(self, obj, **kw):
    #     return http.request.render('meeting_scheduler.object', {
    #         'object': obj
    #     })
    #
    # @route('/meeting_scheduler/guest_view/update/', auth="public", website=True)
    # # request.env['print_table'].create({'show_stuff': 'backend'})
    # def test(self, **kw):
    #     my_input = kw.get('my_input')  # Get the value of the 'my_input' parameter
    #     request.env['print_table'].create({'show_stuff': my_input})
    #     return True
    #
    # @http.route('/my/route', type='http', auth='public')
    # def my_method(self, **post):
    #     my_input = post.get('my_input')  # Get the value of the 'my_input' parameter
    #     # Do something with my_input
    #     request.env['print_table'].create({'show_stuff': str(my_input)})
    #     return "Success"
