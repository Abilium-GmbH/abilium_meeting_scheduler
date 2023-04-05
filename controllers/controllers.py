# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import route, request

class MeetingScheduler(http.Controller):
    @http.route('/meeting_scheduler/meeting_scheduler/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @route('/meeting_scheduler/guest_view/', auth='public', website=True)
    def index(self, **kw):
        records = request.env['timeslots'].sudo().search([])
        # records = request.env['meeting_scheduler'].sudo().search([])
        # request.env['print_table'].create({'show_stuff': records})
        response = request.render("meeting_scheduler.guest_view_loop", {'value': records})
        if((kw.get('firstname') is not None) and (kw.get('firstname') != '')):
            firstname = kw.get('firstname')  # Get the value of the 'my_input' parameter
            request.env['print_table'].create({'show_stuff': firstname})
        return response

    @http.route('/meeting_scheduler/meeting_scheduler/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('meeting_scheduler.listing', {
            'root': '/meeting_scheduler/meeting_scheduler',
            'objects': http.request.env['meeting_scheduler'].search([]),
        })

    @http.route('/meeting_scheduler/meeting_scheduler/objects/<model("meeting_scheduler"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('meeting_scheduler.object', {
            'object': obj
        })

    @route('/meeting_scheduler/guest_view/update/', auth="public", website=True)
    # request.env['print_table'].create({'show_stuff': 'backend'})
    def test(self, **kw):
        my_input = kw.get('my_input')  # Get the value of the 'my_input' parameter
        request.env['print_table'].create({'show_stuff': my_input})
        return True

    @http.route('/my/route', type='http', auth='public')
    def my_method(self, **post):
        my_input = post.get('my_input')  # Get the value of the 'my_input' parameter
        # Do something with my_input
        request.env['print_table'].create({'show_stuff': str(my_input)})
        return "Success"
