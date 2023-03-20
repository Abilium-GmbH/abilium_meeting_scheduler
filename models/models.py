# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api


class meeting_scheduler(models.Model):
    _name = 'meeting_scheduler'
    _description = 'meeting_scheduler'

    meeting_title = fields.Char(string="Meeting Title", required=True)
    meeting_start_date = fields.Datetime(string="Start Date", required=True)
    meeting_end_date = fields.Datetime(string="End Date", required=True)
    meeting_location = fields.Char(string="Location")
    meeting_subject = fields.Text(string="Subject")
    meeting_duration = fields.Char(string="Duration", compute="_calc_duration", store=True)
    meeting_repetitions = fields.Integer(string="Number of repetitions", default=1)
    meeting_frequency = fields.Selection([('0', 'Not repeating'),
                                          ('1', 'Weekly'),
                                          ('2', 'Biweekly')],
                                         store=True, string="Repeating", default='0')
    meeting_privacy = fields.Selection([('public', 'Everyone'),
                                        ('private', 'Only me'),
                                        ('confidential', 'Only internal users')],
                                       'Privacy', default='public', required=True)
    meeting_show_as = fields.Selection([('free', 'Free'),
                                        ('busy', 'Busy')], 'Show Time as', default='busy', required=True)

    @api.depends('meeting_start_date', 'meeting_end_date')
    def _calc_duration(self):

        try:
            for record in self:
                record.meeting_duration = record.meeting_end_date - record.meeting_start_date
        except:
            record.meeting_duration = "Error"

    @api.model_create_multi
    def create(self, data_list):

        #created_records stores all the created records
        created_records = []

        #stores values given in the form for easier calculations and adjustments
        meeting_repetitions = data_list[0]['meeting_repetitions']
        meeting_frequency = data_list[0]['meeting_frequency']
        default_title = data_list[0]['meeting_title']
        default_start_date = data_list[0]['meeting_start_date']

        #frequency 1 is weekly so add 7 days
        if meeting_frequency == '1':

            for x in range(meeting_repetitions):
                data_list[0]['meeting_title'] = default_title + " #" + str(x + 1)

                #datetime is stored as string, so we need to convert string to datetime object then add the days and then convert it back to a string
                data_list[0]['meeting_start_date'] = str(datetime.datetime.strptime(default_start_date,
                                                    "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=7 * x))

                data_list[0]['meeting_end_date'] = str(datetime.datetime.strptime(default_start_date,
                                                    "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=7 * x))

                created_records.append(super(meeting_scheduler, self).create(data_list))
                self.create_entry_to_calendar(data_list[0])

        #frequency 2 is biweekly so add 14 days
        elif meeting_frequency == '2':

            for x in range(meeting_repetitions):
                data_list[0]['meeting_title'] = default_title + " #" + str(x + 1)
                data_list[0]['meeting_start_date'] = str(datetime.datetime.strptime(default_start_date,
                                                    "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=14 * x))

                data_list[0]['meeting_end_date'] = str(datetime.datetime.strptime(default_start_date,
                                                    "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=14 * x))

                created_records.append(super(meeting_scheduler, self).create(data_list))
                self.create_entry_to_calendar(data_list[0])

        #else create normal record
        else:
            created_records.append(super(meeting_scheduler, self).create(data_list))
            self.create_entry_to_calendar(data_list[0])

        #show the first meeting
        return created_records[0]

    def write(self, vals):
        """
        overrides the write function, this enables to update changes from meetings
        in the calendar_event database of the calendar module.
        At the moment it is not yet possible to detect meetings which where deleted
        in the calendar module, editing such a meeting still present in the
        meeting_scheduler module will cause no error and will not create a meeting
        in the calendar module.
        :param vals:
        :return:
        """
        for record in self:
            # the search looks for meetings in the calendar with same name, start, stop
            # this has to be tested and verified how it behaves with identical meetings
            record_found = self.env['calendar.event'].search([('name', '=', record.meeting_title),
                                                              ('privacy', '=', record.meeting_privacy),
                                                              ('show_as', '=', record.meeting_show_as),
                                                              ('start', '=', record.meeting_start_date),
                                                              ('stop', '=', record.meeting_end_date)])
            if(record_found.exists()):
                if(vals.get('meeting_title')):
                    new_meeting_title = vals.get('meeting_title')
                else:
                    new_meeting_title = record.meeting_title

                if (vals.get('meeting_privacy')):
                    new_meeting_privacy = vals.get('meeting_privacy')
                else:
                    new_meeting_privacy = record.meeting_privacy

                if (vals.get('meeting_show_as')):
                    new_meeting_show_as = vals.get('meeting_show_as')
                else:
                    new_meeting_show_as = record.meeting_show_as

                if (vals.get('meeting_start_date')):
                    new_meeting_start_date = vals.get('meeting_start_date')
                else:
                    new_meeting_start_date = record.meeting_start_date

                if (vals.get('meeting_end_date')):
                    new_meeting_end_date = vals.get('meeting_end_date')
                else:
                    new_meeting_end_date = record.meeting_end_date

                # when using vals.get('meeting_title') it only contains a value when changed,
                # if no change to the specific variable then it will cast an error
                # write() makes one single statement in the db calendar_event, update() makes a statement for each entry
                record_found[0].write({'name': new_meeting_title,
                                       'privacy': new_meeting_privacy,
                                       'show_as': new_meeting_show_as,
                                       'start': new_meeting_start_date,
                                       'stop': new_meeting_end_date})
        return super(meeting_scheduler, self).write(vals)



    @api.model
    def create_entry_to_calendar(self, vals):
        """
        creates a new meeting entry in the calendar_event database of the calendar module
        :param vals:
        :return:
        """
        # vals.get() takes the submitted values, as during creation all these values are needed
        self.env['calendar.event'].create({'name': vals.get('meeting_title'),
                                           'privacy': vals.get('meeting_privacy'),
                                           'show_as': vals.get('meeting_show_as'),
                                           'start': vals.get('meeting_start_date'),
                                           'stop': vals.get('meeting_end_date')})
        # self.env.cr.commit() #shows no effect when used or not used
