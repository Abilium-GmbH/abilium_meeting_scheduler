from odoo.tests import common
import datetime
from .. import models


class OverwriteTest(common.TransactionCase):

    def test_overwrite(self):

        meeting_1 = self.env['meeting_scheduler'].create({'meeting_title': 'test meeting',
                                                          'meeting_repetitions': 1,
                                                          'meeting_frequency': '0',
                                                          'meeting_start_date':
                                                              datetime.datetime(2023, 3, 31, 15, 0, 0),
                                                          'meeting_end_date':
                                                              datetime.datetime(2023, 3, 31, 16, 0, 0),
                                                          'meeting_location': 'here',
                                                          'meeting_subject': 'test',
                                                          'meeting_privacy': 'public',
                                                          'meeting_show_as': 'busy'})

        meeting_2 = self.env['meeting_scheduler'].create({'meeting_title': 'test meeting 2',
                                                          'meeting_repetitions': 2,
                                                          'meeting_frequency': '0',
                                                          'meeting_start_date':
                                                              datetime.datetime(2023, 5, 28, 15, 0, 0),
                                                          'meeting_end_date':
                                                              datetime.datetime(2023, 5, 28, 16, 0, 0),
                                                          'meeting_location': 'nowhere',
                                                          'meeting_subject': 'run',
                                                          'meeting_privacy': 'public',
                                                          'meeting_show_as': 'busy'})

        new_title = 'new title'
        new_repetitions = 2
        new_frequency = '2'
        new_start_date = datetime.datetime(2023, 3, 31, 20, 0, 0)
        new_end_date = datetime.datetime(2023, 3, 31, 21, 0, 0)
        new_location = 'there'
        new_subject = 'revise'
        new_privacy = 'private'
        new_show_as = 'free'

        new_vals = {'meeting_title': new_title,
                    'meeting_repetitions': new_repetitions,
                    'meeting_frequency': new_frequency,
                    'meeting_start_date': new_start_date,
                    'meeting_end_date': new_end_date,
                    'meeting_location': new_location,
                    'meeting_subject': new_subject,
                    'meeting_privacy': new_privacy,
                    'meeting_show_as': new_show_as}

        no_vals = {'meeting_location': new_location}

        calendar_event_1 = self.env['calendar.event'].search([('name', '=', 'test meeting')])

        self.assertEqual(calendar_event_1.name, 'test meeting')

        meeting_1.write(new_vals)

        self.assertEqual(calendar_event_1.name, new_title)

        calendar_event_2 = self.env['calendar.event'].search([('name', '=', 'test meeting 2')])

        self.assertEqual(calendar_event_2.name, 'test meeting 2')

        meeting_2.write(no_vals)

        self.assertEqual(calendar_event_2.name, 'test meeting 2')
