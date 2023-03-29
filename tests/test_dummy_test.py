from odoo.tests import common
import datetime
from .. import models

class DummyTest(common.TransactionCase):

    def test_dummy_test_1(self):

        meeting_1 = self.env['meeting_scheduler'].create({'meeting_title': 'test meeting',
                                                          'meeting_repetitions': 1,
                                                          'meeting_frequency': '0',
                                                          'meeting_start_date':
                                                              datetime.datetime.strptime("2023-03-29 15:00:00", "%Y-%m-%d %H:%M:%S"),
                                                          'meeting_end_date':
                                                              datetime.datetime.strptime("2023-03-29 17:00:00", "%Y-%m-%d %H:%M:%S"),
                                                          'meeting_location': 'airport',
                                                          'meeting_subject': 'testing',
                                                          'meeting_privacy': 'public',
                                                          'meeting_show_as': 'busy'})
        #get actual values of meeting_1
        actual_title = meeting_1.get_title()
        actual_repetitions = meeting_1.get_repetitions()
        actual_frequency = meeting_1.get_frequency()
        actual_start_date = meeting_1.get_start_date()
        actual_end_date = meeting_1.get_end_date()
        actual_duration = meeting_1.get_duration()
        actual_location = meeting_1.get_location()
        actual_subject = meeting_1.get_subject()
        actual_privacy = meeting_1.get_privacy()
        actual_show_as = meeting_1.get_show_as()

        #check if meeting_1 was created correctly
        self.assertEqual("test meeting", actual_title)
        self.assertEqual(1, actual_repetitions)
        self.assertEqual('0', actual_frequency)
        self.assertEqual("airport", actual_location)
        self.assertEqual("testing", actual_subject)
        self.assertEqual("public", actual_privacy)
        self.assertEqual('busy', actual_show_as)
        self.assertEqual('2:00:00', actual_duration)
        self.assertEqual(datetime.datetime(2023, 3, 29, 15, 00, 00), actual_start_date)
        self.assertEqual(datetime.datetime(2023, 3, 29, 17, 00, 00), actual_end_date)

