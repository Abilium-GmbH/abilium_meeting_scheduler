# -*- coding: utf-8 -*-
from odoo import http


class MeetingScheduler(http.Controller):
    @http.route('/meeting__scheduler/meeting__scheduler/', auth='public')
    def index(self, **kw):
       return "Hello, world"

    @http.route('/meeting__scheduler/meeting__scheduler/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('meeting__scheduler.listing', {
            'root': '/meeting__scheduler/meeting__scheduler',
            'objects': http.request.env['meeting__scheduler.meeting__scheduler'].search([]),
        })

    @http.route('/meeting__scheduler/meeting__scheduler/objects/<model("meeting__scheduler.meeting__scheduler"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('meeting__scheduler.object', {
           'object': obj
        })
