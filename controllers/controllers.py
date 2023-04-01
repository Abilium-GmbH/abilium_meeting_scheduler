# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import route, request

class MeetingScheduler(http.Controller):
    @http.route('/meeting_scheduler/meeting_scheduler/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @route('/meeting_scheduler/guest_view/', auth='public', website=True)
    def index(self, **kw):
        records = request.env['meeting_scheduler'].sudo().search([])
        response = request.render("meeting_scheduler.jkdfjk")
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
