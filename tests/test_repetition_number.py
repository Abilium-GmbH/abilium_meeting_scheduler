from odoo.tests import common
import datetime


class DurationTest(common.TransactionCase):

    def test_error_weekly(self):

        # tests for reps = 0
        data_list_0 = {'meeting_title': 'weekly',
                       'meeting_repetitions': 0,
                       'meeting_frequency': '1',
                       'meeting_start_date':
                           datetime.datetime.strptime("2023-03-29 15:00:00",
                                                      "%Y-%m-%d %H:%M:%S"),
                       'meeting_end_date':
                           datetime.datetime.strptime("2023-03-29 17:00:00",
                                                      "%Y-%m-%d %H:%M:%S"),
                       'meeting_location': 'airport',
                       'meeting_subject': 'testing',
                       'meeting_privacy': 'public',
                       'meeting_show_as': 'busy'}

        with self.assertRaises(IndexError):
            self.env['meeting_scheduler'].create(data_list_0)

        # tests for reps = -1
        data_list_1 = {'meeting_title': 'weekly',
                       'meeting_repetitions': -1,
                       'meeting_frequency': '1',
                       'meeting_start_date':
                           datetime.datetime.strptime("2023-03-29 15:00:00",
                                                      "%Y-%m-%d %H:%M:%S"),
                       'meeting_end_date':
                           datetime.datetime.strptime("2023-03-29 17:00:00",
                                                      "%Y-%m-%d %H:%M:%S"),
                       'meeting_location': 'airport',
                       'meeting_subject': 'testing',
                       'meeting_privacy': 'public',
                       'meeting_show_as': 'busy'}

        with self.assertRaises(IndexError):
            self.env['meeting_scheduler'].create(data_list_1)

    def test_error_biweekly(self):

        # tests for reps = 0
        data_list_0 = {'meeting_title': 'biweekly',
                       'meeting_repetitions': 0,
                       'meeting_frequency': '2',
                       'meeting_start_date':
                           datetime.datetime.strptime("2023-03-29 15:00:00",
                                                      "%Y-%m-%d %H:%M:%S"),
                       'meeting_end_date':
                           datetime.datetime.strptime("2023-03-29 17:00:00",
                                                      "%Y-%m-%d %H:%M:%S"),
                       'meeting_location': 'airport',
                       'meeting_subject': 'testing',
                       'meeting_privacy': 'public',
                       'meeting_show_as': 'busy'}

        with self.assertRaises(IndexError):
            self.env['meeting_scheduler'].create(data_list_0)

        # tests for reps = -1
        data_list_1 = {'meeting_title': 'biweekly',
                       'meeting_repetitions': -1,
                       'meeting_frequency': '2',
                       'meeting_start_date':
                           datetime.datetime.strptime("2023-03-29 15:00:00",
                                                      "%Y-%m-%d %H:%M:%S"),
                       'meeting_end_date':
                           datetime.datetime.strptime("2023-03-29 17:00:00",
                                                      "%Y-%m-%d %H:%M:%S"),
                       'meeting_location': 'airport',
                       'meeting_subject': 'testing',
                       'meeting_privacy': 'public',
                       'meeting_show_as': 'busy'}

        with self.assertRaises(IndexError):
            self.env['meeting_scheduler'].create(data_list_1)

    def test_numbers(self):
        data_list_1 = {'meeting_title': 'weekly',
                       'meeting_repetitions': 50,
                       'meeting_frequency': '1',
                       'meeting_start_date':
                           str(datetime.datetime.strptime("2023-03-29 15:00:00",
                                                          "%Y-%m-%d %H:%M:%S")),
                       'meeting_end_date':
                           str(datetime.datetime.strptime("2023-03-29 17:00:00",
                                                          "%Y-%m-%d %H:%M:%S")),
                       'meeting_location': 'airport',
                       'meeting_subject': 'testing',
                       'meeting_privacy': 'public',
                       'meeting_show_as': 'busy'}

        data_list_2 = {'meeting_title': 'biweekly',
                       'meeting_repetitions': 50,
                       'meeting_frequency': '2',
                       'meeting_start_date':
                           str(datetime.datetime.strptime("2023-03-29 15:00:00",
                                                          "%Y-%m-%d %H:%M:%S")),
                       'meeting_end_date':
                           str(datetime.datetime.strptime("2023-03-29 17:00:00",
                                                          "%Y-%m-%d %H:%M:%S")),
                       'meeting_location': 'airport',
                       'meeting_subject': 'testing',
                       'meeting_privacy': 'public',
                       'meeting_show_as': 'busy'}

        self.env['meeting_scheduler'].create(data_list_1)
        self.env['meeting_scheduler'].create(data_list_2)

        # test if all weekly meetings exist
        for i in range(1, 51):
            name = "weekly #" + str(i)
            meeting = self.env['meeting_scheduler'].search([('meeting_title', '=', name)])

            self.assertNotEqual(meeting.meeting_title, False)

        # test if all biweekly meetings exist
        for i in range(1, 51):
            name = "biweekly #" + str(i)
            meeting = self.env['meeting_scheduler'].search([('meeting_title', '=', name)])

            self.assertNotEqual(meeting.meeting_title, False)
