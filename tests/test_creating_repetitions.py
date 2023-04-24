from odoo.tests import common
import datetime


class RepeatingMeetingTest(common.TransactionCase):

    def test_weekly_creation(self):
        meeting_weekly = self.env['meeting_scheduler'].create({'meeting_title': 'weekly',
                                                               'meeting_repetitions': 3,
                                                               'meeting_frequency': '1',
                                                               'meeting_start_date':
                                                                   "2023-4-1 16:0:0",
                                                               'meeting_end_date':
                                                                   "2023-4-1 18:0:0",
                                                               'meeting_location': 'airport',
                                                               'meeting_subject': 'testing',
                                                               'meeting_privacy': 'public',
                                                               'meeting_show_as': 'busy'})

        week_1 = self.env['meeting_scheduler'].search([('meeting_title', '=', 'weekly #1')])
        week_2 = self.env['meeting_scheduler'].search([('meeting_title', '=', 'weekly #2')])
        week_3 = self.env['meeting_scheduler'].search([('meeting_title', '=', 'weekly #3')])

        # test week_1
        self.assertEqual(week_1.meeting_start_date, datetime.datetime(2023, 4, 1, 16, 0, 0))
        self.assertEqual(week_1.meeting_end_date, datetime.datetime(2023, 4, 1, 18, 0, 0))
        self.assertEqual(week_1.meeting_duration, "2:00:00")
        self.assertEqual(week_1.meeting_repetitions, 3)
        self.assertEqual(week_1.meeting_frequency, "1")

        # test week_2
        self.assertEqual(week_2.meeting_start_date, datetime.datetime(2023, 4, 8, 16, 0, 0))
        self.assertEqual(week_2.meeting_end_date, datetime.datetime(2023, 4, 8, 18, 0, 0))
        self.assertEqual(week_2.meeting_duration, "2:00:00")
        self.assertEqual(week_2.meeting_repetitions, 3)
        self.assertEqual(week_2.meeting_frequency, "1")

        # test week_3
        self.assertEqual(week_3.meeting_start_date, datetime.datetime(2023, 4, 15, 16, 0, 0))
        self.assertEqual(week_3.meeting_end_date, datetime.datetime(2023, 4, 15, 18, 0, 0))
        self.assertEqual(week_3.meeting_duration, "2:00:00")
        self.assertEqual(week_3.meeting_repetitions, 3)
        self.assertEqual(week_3.meeting_frequency, "1")

    def test_biweekly_creation(self):
        meeting_biweekly = self.env['meeting_scheduler'].create({'meeting_title': 'biweekly',
                                                                 'meeting_repetitions': 3,
                                                                 'meeting_frequency': '2',
                                                                 'meeting_start_date':
                                                                     "2023-4-1 16:0:0",
                                                                 'meeting_end_date':
                                                                     "2023-4-1 18:0:0",
                                                                 'meeting_location': 'airport',
                                                                 'meeting_subject': 'testing',
                                                                 'meeting_privacy': 'public',
                                                                 'meeting_show_as': 'busy'})

        week_1 = self.env['meeting_scheduler'].search([('meeting_title', '=', 'biweekly #1')])
        week_2 = self.env['meeting_scheduler'].search([('meeting_title', '=', 'biweekly #2')])
        week_3 = self.env['meeting_scheduler'].search([('meeting_title', '=', 'biweekly #3')])

        # test week_1
        self.assertEqual(week_1.meeting_start_date, datetime.datetime(2023, 4, 1, 16, 0, 0))
        self.assertEqual(week_1.meeting_end_date, datetime.datetime(2023, 4, 1, 18, 0, 0))
        self.assertEqual(week_1.meeting_duration, "2:00:00")
        self.assertEqual(week_1.meeting_repetitions, 3)
        self.assertEqual(week_1.meeting_frequency, "2")

        # test week_2
        self.assertEqual(week_2.meeting_start_date, datetime.datetime(2023, 4, 15, 16, 0, 0))
        self.assertEqual(week_2.meeting_end_date, datetime.datetime(2023, 4, 15, 18, 0, 0))
        self.assertEqual(week_2.meeting_duration, "2:00:00")
        self.assertEqual(week_2.meeting_repetitions, 3)
        self.assertEqual(week_2.meeting_frequency, "2")

        # test week_3
        self.assertEqual(week_3.meeting_start_date, datetime.datetime(2023, 4, 29, 16, 0, 0))
        self.assertEqual(week_3.meeting_end_date, datetime.datetime(2023, 4, 29, 18, 0, 0))
        self.assertEqual(week_3.meeting_duration, "2:00:00")
        self.assertEqual(week_3.meeting_repetitions, 3)
        self.assertEqual(week_3.meeting_frequency, "2")
