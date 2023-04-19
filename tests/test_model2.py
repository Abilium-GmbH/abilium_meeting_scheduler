from odoo.tests import common
import pytz
import datetime


class Model2Test(common.TransactionCase):

    def test_button_function(self):
        print("TODO")

    def test_algo02(self):
        print("TODO")

    def test_find_overlapping_timeslots(self):

        group_scheduler_0 = self.env['group_scheduler'].create({'meeting_group': 'test group'})

        #2 slots with
        timeslots0 = [[datetime.datetime(2023, 4, 10, 10, 0, 0), datetime.datetime(2023, 4, 10, 20, 0, 0)],
                      [datetime.datetime(2023, 4, 10, 11, 0, 0), datetime.datetime(2023, 4, 10, 19, 0, 0)]]

        result0 = str(group_scheduler_0.find_overlapping_timeslots(timeslots0))
        expected0 = "(datetime.datetime(2023, 4, 10, 11, 0), datetime.datetime(2023, 4, 10, 19, 0))"
        self.assertEqual(result0, expected0)

        #2 slots without
        """
        Throws error:
        File "/usr/lib/python3/dist-packages/odoo/addons/meeting_scheduler/tests/test_model2.py", line 30, in test_find_overlapping_timeslots
            result1 = str(group_scheduler_0.find_overlapping_timeslots(timeslots1))
        File "/usr/lib/python3/dist-packages/odoo/addons/meeting_scheduler/models/models2.py", line 205, in find_overlapping_timeslots
            return otuput_overlaps
        UnboundLocalError: local variable 'otuput_overlaps' referenced before assignment
        
        Fix:
        Already in models2.py line 190
        """
        
        timeslots1 = [[datetime.datetime(2023, 4, 10, 12, 0, 0), datetime.datetime(2023, 4, 10, 18, 0, 0)],
                      [datetime.datetime(2023, 4, 10, 9, 0, 0), datetime.datetime(2023, 4, 10, 12, 0, 0)]]

        result1 = str(group_scheduler_0.find_overlapping_timeslots(timeslots1))
        expected1 = "None"
        self.assertEqual(result1, expected1)

        #3 slots with
        timeslots2 = [[datetime.datetime(2023, 4, 10, 6, 0, 0), datetime.datetime(2023, 4, 10, 18, 0, 0)],
                      [datetime.datetime(2023, 4, 10, 7, 0, 0), datetime.datetime(2023, 4, 10, 19, 0, 0)],
                      [datetime.datetime(2023, 4, 10, 9, 0, 0), datetime.datetime(2023, 4, 10, 17, 0, 0)]]

        result2 = str(group_scheduler_0.find_overlapping_timeslots(timeslots2))
        expected2 = "(datetime.datetime(2023, 4, 10, 9, 0), datetime.datetime(2023, 4, 10, 17, 0))"
        self.assertEqual(result2, expected2)

        #3 slots without
        """
        This test fails. If this function is supposed to return a overlapping timeslot of all the given times then it
        doesnt work correctly. It returns the following timeslot instead of None:
            10:00 - 18:00
            
        I think this is because it only checks for the predecessor and not all previous slots.
        """
        timeslots3 = [[datetime.datetime(2023, 4, 10, 6, 0, 0), datetime.datetime(2023, 4, 10, 10, 0, 0)], #6:00 - 10:00
                      [datetime.datetime(2023, 4, 10, 7, 0, 0), datetime.datetime(2023, 4, 10, 18, 0, 0)], #7:00 - 18:00
                      [datetime.datetime(2023, 4, 10, 10, 0, 0), datetime.datetime(2023, 4, 10, 19, 0, 0)]] #10:00 - 19:00

        result3 = str(group_scheduler_0.find_overlapping_timeslots(timeslots3))
        expected3 = "None"
        self.assertEqual(result3, expected3)


    def test_convert_timezones(self):

        """
        Most of these Tests don't work with the current implementation of convert_timeone(). A fix has been added
        as a comment in order to not disturbe any unseen uses of this funtion that currently work.
        """

        group_scheduler_0 = self.env['group_scheduler'].create({'meeting_group': 'test group'})

        #Test Chicago
        chicagoTime = datetime.datetime.now(pytz.timezone('America/Chicago'))

        expectedChicago = (chicagoTime + datetime.timedelta(hours=7)).strftime("%Y-%m-%d %H:%M:%S")
        resultChicago = group_scheduler_0.convert_timezone(chicagoTime).strftime("%Y-%m-%d %H:%M:%S")

        self.assertEqual(expectedChicago, resultChicago)

        #Test Timbuktu
        timbuktuTime = datetime.datetime.now(pytz.timezone('Africa/Timbuktu'))

        expectedTimbuktu = (timbuktuTime + datetime.timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")
        resultTimbuktu = group_scheduler_0.convert_timezone(timbuktuTime).strftime("%Y-%m-%d %H:%M:%S")

        self.assertEqual(expectedTimbuktu, resultTimbuktu)

        #Test Bangkok
        bangkokTime = datetime.datetime.now(pytz.timezone('Asia/Bangkok'))

        expectedBangkok = (bangkokTime + datetime.timedelta(hours=-5)).strftime("%Y-%m-%d %H:%M:%S")
        resultBangkok = group_scheduler_0.convert_timezone(bangkokTime).strftime("%Y-%m-%d %H:%M:%S")

        self.assertEqual(expectedBangkok, resultBangkok)

        #Test Same
        localTime = datetime.datetime.now(pytz.timezone(self.env.context.get('tz') or self.env.user.tz))

        expectedLocal = localTime.strftime("%Y-%m-%d %H:%M:%S")
        resultLocal = group_scheduler_0.convert_timezone(localTime).strftime("%Y-%m-%d %H:%M:%S")

        self.assertEqual(expectedLocal, resultLocal)




