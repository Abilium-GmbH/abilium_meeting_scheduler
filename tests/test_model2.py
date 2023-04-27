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
        timeslots3 = [[datetime.datetime(2023, 4, 10, 6, 0, 0), datetime.datetime(2023, 4, 10, 10, 0, 0)],
                      [datetime.datetime(2023, 4, 10, 7, 0, 0), datetime.datetime(2023, 4, 10, 18, 0, 0)],
                      [datetime.datetime(2023, 4, 10, 10, 0, 0), datetime.datetime(2023, 4, 10, 19, 0, 0)]]

        result3 = str(group_scheduler_0.find_overlapping_timeslots(timeslots3))
        expected3 = "None"
        self.assertEqual(result3, expected3)

        #2 slots with and diff tz

        chicagoStart = datetime.datetime(2023, 4, 10, 6, 0, 0, 0)
        chicagoStartTZ = pytz.timezone('America/Chicago').localize(chicagoStart)
        chicagoEnd = datetime.datetime(2023, 4, 10, 16, 0, 0, 0)
        chicagoEndTZ = pytz.timezone('America/Chicago').localize(chicagoEnd)

        timbuktuStart = datetime.datetime(2023, 4, 10, 6, 0, 0, 0)
        timbuktuStartTZ = pytz.timezone('Africa/Timbuktu').localize(timbuktuStart)
        timbuktuEnd = datetime.datetime(2023, 4, 10, 20, 0, 0, 0)
        timbuktuEndTZ = pytz.timezone('Africa/Timbuktu').localize(timbuktuEnd)
        timeslots4 = [[chicagoStartTZ, chicagoEndTZ],
                      [timbuktuStartTZ, timbuktuEndTZ]]

        result4 = str(group_scheduler_0.find_overlapping_timeslots(timeslots4))
        expected4 = "(datetime.datetime(2023, 4, 10, 13, 0), datetime.datetime(2023, 4, 10, 22, 0))"
        self.assertEqual(result4, expected4)

        #no slots
        timeslots5 = [[],[]]

        result5 = str(group_scheduler_0.find_overlapping_timeslots(timeslots5))
        expected5 = "None"
        self.assertEqual(result5, expected5)

        #wrong inputs
        timeslots6 = [[datetime.datetime(2023, 10, 4, 15, 30), datetime.datetime(2023, 10, 4, 19, 45)], []]
        result6 = str(group_scheduler_0.find_overlapping_timeslots(timeslots6))
        expected6 = "None"

        self.assertEqual(result6, expected6)

        timeslots7 = [[], [datetime.datetime(2023, 10, 4, 15, 30), datetime.datetime(2023, 10, 4, 19, 45)]]
        result7 = str(group_scheduler_0.find_overlapping_timeslots(timeslots7))
        expected7 = "None"

        self.assertEqual(result7, expected7)

        timeslots8 = [[datetime.datetime(2023, 10, 4, 15, 30)], [datetime.datetime(2023, 10, 4, 19, 45)]]
        result8 = str(group_scheduler_0.find_overlapping_timeslots(timeslots8))
        expected8 = "None"

        self.assertEqual(result8, expected8)

        timeslots9 = [[datetime.datetime(2023, 4, 10, 6, 0, 0), datetime.datetime(2023, 4, 10, 18, 0, 0)],
                      [datetime.datetime(2023, 4, 10, 7, 0, 0), datetime.datetime(2023, 4, 10, 19, 0, 0)],
                      [datetime.datetime(2023, 4, 10, 9, 0, 0), datetime.datetime(2023, 4, 10, 17, 0, 0), datetime.datetime(2023, 4, 10, 11, 30, 0)]]
        result9 = str(group_scheduler_0.find_overlapping_timeslots(timeslots9))
        expected9 = "None"

        self.assertEqual(result9, expected9)


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

        #Test no tz
        noTZtime = datetime.datetime(2023, 4, 13, 20, 30, 0)

        expectedNoTZ = noTZtime.strftime("%Y-%m-%d %H:%M:%S")
        resultNoTZ = group_scheduler_0.convert_timezone(noTZtime).strftime("%Y-%m-%d %H:%M:%S")

        self.assertEqual(expectedNoTZ, resultNoTZ)




