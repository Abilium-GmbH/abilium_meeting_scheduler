from odoo.tests import common
import datetime
from .. import models

class CalendarCreationTest(common.TransactionCase):

    def test_calendar_event_creation(self):

        meeting_1 = self.env['meeting_scheduler'].create({'meeting_title': 'calendar event 1',
                                                          'meeting_repetitions': 1,
                                                          'meeting_frequency': '0',
                                                          'meeting_start_date':
                                                              datetime.datetime(2023, 3, 31, 15, 0, 0),
                                                          'meeting_end_date':
                                                              datetime.datetime(2023, 3, 31, 16, 0, 0),
                                                          'meeting_location': 'airport',
                                                          'meeting_subject': 'testing',
                                                          'meeting_privacy': 'public',
                                                          'meeting_show_as': 'busy'})

        meeting_2 = self.env['meeting_scheduler'].create({'meeting_title': 'calendar event 2',
                                                          'meeting_repetitions': 1,
                                                          'meeting_frequency': '0',
                                                          'meeting_start_date':
                                                              datetime.datetime(2023, 3, 31, 17, 0, 0),
                                                          'meeting_end_date':
                                                              datetime.datetime(2023, 3, 31, 19, 0, 0),
                                                          'meeting_location': 'airport',
                                                          'meeting_subject': 'testing',
                                                          'meeting_privacy': 'public',
                                                          'meeting_show_as': 'busy'})


        calendar_event_1 = self.env['calendar.event'].search([('name', '=', 'calendar event 1')])
        calendar_event_2 = self.env['calendar.event'].search([('name', '=', 'calendar event 2')])

        event_1_title = calendar_event_1.name
        event_1_privacy = calendar_event_1.privacy
        event_1_show_as = calendar_event_1.show_as
        event_1_start = calendar_event_1.start
        event_1_stop = calendar_event_1.stop

        self.assertEqual(event_1_title, meeting_1.meeting_title)
        self.assertEqual(event_1_privacy, meeting_1.meeting_privacy)
        self.assertEqual(event_1_show_as, meeting_1.meeting_show_as)
        self.assertEqual(event_1_start, meeting_1.meeting_start_date)
        self.assertEqual(event_1_stop, meeting_1.meeting_end_date)

        event_2_title = calendar_event_2.name
        event_2_privacy = calendar_event_2.privacy
        event_2_show_as = calendar_event_2.show_as
        event_2_start = calendar_event_2.start
        event_2_stop = calendar_event_2.stop

        self.assertEqual(event_2_title, meeting_2.meeting_title)
        self.assertEqual(event_2_privacy, meeting_2.meeting_privacy)
        self.assertEqual(event_2_show_as, meeting_2.meeting_show_as)
        self.assertEqual(event_2_start, meeting_2.meeting_start_date)
        self.assertEqual(event_2_stop, meeting_2.meeting_end_date)

    def test_same_name_event(self):

        meeting = self.env['meeting_scheduler'].create({'meeting_title': 'calendar event',
                                                          'meeting_repetitions': 1,
                                                          'meeting_frequency': '0',
                                                          'meeting_start_date':
                                                              datetime.datetime(2023, 5, 10, 10, 0, 0),
                                                          'meeting_end_date':
                                                              datetime.datetime(2023, 5, 10, 11, 0, 0),
                                                          'meeting_location': 'airport',
                                                          'meeting_subject': 'testing',
                                                          'meeting_privacy': 'public',
                                                          'meeting_show_as': 'busy'})

        with self.assertRaises(ValueError):
            meeting_same = self.env['meeting_scheduler'].create({'meeting_title': 'calendar event',
                                                                'meeting_repetitions': 1,
                                                                'meeting_frequency': '0',
                                                                'meeting_start_date':
                                                                     datetime.datetime(2023, 5, 10, 10, 0, 0),
                                                                'meeting_end_date':
                                                                     datetime.datetime(2023, 5, 10, 11, 0, 0),
                                                                'meeting_location': 'airport',
                                                                'meeting_subject': 'testing',
                                                                'meeting_privacy': 'public',
                                                                'meeting_show_as': 'busy'})
