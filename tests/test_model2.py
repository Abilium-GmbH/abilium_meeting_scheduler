from odoo.tests import common
import pytz
import datetime


class Model2Test(common.TransactionCase):

    def test_button_function(self):
        print("TODO")

    def test_algo02(self):
        print("TODO")

    def test_find_overlapping_timeslots(self):
        print("TODO")

    def test_convert_timezones(self):

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



