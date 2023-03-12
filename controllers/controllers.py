# -*- coding: utf-8 -*-
from odoo import http


class MeetingScheduler(http.Controller):
    @http.route('/meeting_scheduler/meeting_scheduler/', auth='public')
    def index(self, **kw):
        return "Hello, world"

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
