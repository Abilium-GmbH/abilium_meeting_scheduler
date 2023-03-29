from odoo.tests import common
import datetime

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

        self.assertTrue(False)
