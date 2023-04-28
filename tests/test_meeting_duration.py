from odoo.tests import common
import datetime
from .. import models

class DurationTest(common.TransactionCase):

    def test_duration(self):

        #create test objects
        meeting_1 = self.env['meeting_scheduler'].create({'meeting_title': 'test meeting 1',
                                                          'meeting_repetitions': 1,
                                                          'meeting_frequency': '0',
                                                          'meeting_start_date':
                                                              datetime.datetime(2023, 3, 29, 15, 0, 0),
                                                          'meeting_end_date':
                                                              datetime.datetime(2023, 3, 29, 17, 0, 0),
                                                          'meeting_location': 'airport',
                                                          'meeting_subject': 'testing',
                                                          'meeting_privacy': 'public',
                                                          'meeting_show_as': 'busy'})

        meeting_2 = self.env['meeting_scheduler'].create({'meeting_title': 'test meeting 2',
                                                          'meeting_repetitions': 1,
                                                          'meeting_frequency': '0',
                                                          'meeting_start_date':
                                                              datetime.datetime(2023, 3, 28, 15, 0, 0),
                                                          'meeting_end_date':
                                                              datetime.datetime(2023, 3, 29, 15, 0, 0),
                                                          'meeting_location': 'airport',
                                                          'meeting_subject': 'testing',
                                                          'meeting_privacy': 'public',
                                                          'meeting_show_as': 'busy'})


        meeting_3 = self.env['meeting_scheduler'].create({'meeting_title': 'test meeting 2',
                                                          'meeting_repetitions': 1,
                                                          'meeting_frequency': '0',
                                                          'meeting_start_date':
                                                              datetime.datetime(2023, 3, 29, 15, 0, 0),
                                                          'meeting_end_date':
                                                              datetime.datetime(2023, 3, 29, 15, 0, 0),
                                                          'meeting_location': 'airport',
                                                          'meeting_subject': 'testing',
                                                          'meeting_privacy': 'public',
                                                          'meeting_show_as': 'busy'})
        #get actual values of objects
        m1_actual_start_date = meeting_1.meeting_start_date
        m1_actual_end_date = meeting_1.meeting_end_date
        m1_actual_duration = meeting_1.meeting_duration

        m2_actual_start_date = meeting_2.meeting_start_date
        m2_actual_end_date = meeting_2.meeting_end_date
        m2_actual_duration = meeting_2.meeting_duration

        m3_actual_start_date = meeting_3.meeting_start_date
        m3_actual_end_date = meeting_3.meeting_end_date
        m3_actual_duration = meeting_3.meeting_duration


        #check that there are meetings
        self.assertTrue(self.env['meeting_scheduler'].search([]))

        #check if duration was calculated correctly

        #meeting_1
        self.assertEqual('2:00:00', m1_actual_duration)
        self.assertEqual(datetime.datetime(2023, 3, 29, 15, 00, 00), m1_actual_start_date)
        self.assertEqual(datetime.datetime(2023, 3, 29, 17, 00, 00), m1_actual_end_date)

        #meeting_2
        self.assertEqual('1 day, 0:00:00', m2_actual_duration)
        self.assertEqual(datetime.datetime(2023, 3, 28, 15, 00, 00), m2_actual_start_date)
        self.assertEqual(datetime.datetime(2023, 3, 29, 15, 00, 00), m2_actual_end_date)

        #meeting_3
        self.assertEqual('0:00:00', m3_actual_duration)
        self.assertEqual(datetime.datetime(2023, 3, 29, 15, 00, 00), m3_actual_start_date)
        self.assertEqual(datetime.datetime(2023, 3, 29, 15, 00, 00), m3_actual_end_date)
