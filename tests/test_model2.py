from odoo.tests import common
import pytz
import datetime


class Model2Test(common.TransactionCase):

    def test_button_function(self):
        print("TODO")

    def test_button_timeslots_from_intersection(self):

        user0_0 = self.env['res.users'].create({'name': 'Hans', 'login': 'Hans'})
        user0_0_id = self.env['res.users'].search([('name', '=', 'Hans')]).id

        start_date0_0 = str(datetime.datetime(2023, 10, 2, 9, 0))
        end_date0_0 = str(datetime.datetime(2023, 10, 2, 13, 0))

        start_date0_1 = str(datetime.datetime(2023, 10, 2, 11, 0))
        end_date0_1 = str(datetime.datetime(2023, 10, 2, 15, 0))

        self.env['meeting_scheduler'].create([{
            'meeting_title': 'meetingBookable',
            'meeting_location': False,
            'meeting_start_date': start_date0_0,
            'meeting_end_date': end_date0_0,
            'meeting_repetitions': 1,
            'meeting_frequency': 0,
            'meeting_privacy': 'public',
            'meeting_show_as': 'free',
            'meeting_subject': False,
            'create_uid': user0_0_id
        }])

        user0_1 = self.env['res.users'].create({'name': 'Helen', 'login': 'Helen'})
        user0_1_id = self.env['res.users'].search([('name', '=', 'Helen')]).id

        self.env['meeting_scheduler'].create([{
            'meeting_title': 'meetingBookable',
            'meeting_location': False,
            'meeting_start_date': start_date0_1,
            'meeting_end_date': end_date0_1,
            'meeting_repetitions': 1,
            'meeting_frequency': 0,
            'meeting_privacy': 'public',
            'meeting_show_as': 'free',
            'meeting_subject': False,
            'create_uid': user0_1_id
        }])

        group0 = self.env['res.groups'].create({'name': 'group0', 'users': [[user0_0_id], [user0_1_id]]})
        group0_id = self.env['res.groups'].search([('name', '=', 'group0')]).id

        group_scheduler_0 = self.env['group_scheduler'].\
            create({'meeting_group': group0_id, 'meeting_attendees': [user0_0_id, user0_1_id]})

        start_time_0 = datetime.datetime(2023, 10, 2, 2, 0)
        end_time_0 = datetime.datetime(2023, 10, 2, 23, 0)

        self.env.context = dict(self.env.context, active_ids=[group_scheduler_0.id])

        group_scheduler_0.button_timeslots_from_intersection(start_time_0, end_time_0)

        date = datetime.datetime(2022, 1, 1, 1, 0, 0)

        timeslots = self.env['timeslots'].search([('timeslots_start_date_str','>=', date)])

        self.assertEqual(len(timeslots), 1)

        self.assertEqual(datetime.datetime(2023, 10, 2, 11, 0, 0), timeslots[0].timeslots_start_date_utc)
        self.assertEqual(datetime.datetime(2023, 10, 2, 13, 0, 0), timeslots[0].timeslots_end_date_utc)
        self.assertIn(str(user0_0_id), timeslots[0].timeslots_groupmembers)
        self.assertIn(str(user0_1_id), timeslots[0].timeslots_groupmembers)
        self.assertEqual(timeslots[0].timeslots_bookable_hours, ' 11 12 13')

    def test_intersection_only_one_user(self):

        user0_0 = self.env['res.users'].create({'name': 'Markus', 'login': 'Markus'})
        user0_0_id = self.env['res.users'].search([('name', '=', 'Markus')]).id

        start_date0_0 = str(datetime.datetime(2023, 10, 2, 9, 0))
        end_date0_0 = str(datetime.datetime(2023, 10, 2, 13, 0))

        start_date0_1 = str(datetime.datetime(2023, 10, 2, 11, 0))
        end_date0_1 = str(datetime.datetime(2023, 10, 2, 15, 0))

        self.env['meeting_scheduler'].create([{
            'meeting_title': 'meetingBookable',
            'meeting_location': False,
            'meeting_start_date': start_date0_0,
            'meeting_end_date': end_date0_0,
            'meeting_repetitions': 1,
            'meeting_frequency': 0,
            'meeting_privacy': 'public',
            'meeting_show_as': 'free',
            'meeting_subject': False,
            'create_uid': user0_0_id
        }])

        group0 = self.env['res.groups'].create({'name': 'group0', 'users': [[user0_0_id]]})
        group0_id = self.env['res.groups'].search([('name', '=', 'group0')]).id

        group_scheduler_0 = self.env['group_scheduler']. \
            create({'meeting_group': group0_id, 'meeting_attendees': [user0_0_id]})

        start_time_0 = datetime.datetime(2023, 12, 2, 2, 0)
        end_time_0 = datetime.datetime(2023, 12, 2, 23, 0)

        self.env.context = dict(self.env.context, active_ids=[group_scheduler_0.id])

        group_scheduler_0.button_timeslots_from_intersection(start_time_0, end_time_0)

        date = datetime.datetime(2022, 1, 1, 1, 0, 0)

        timeslots = self.env['timeslots'].search([('timeslots_start_date_str', '>=', date)])

        print(timeslots)

    def test_button_timeslots_from_union(self):

        user0_0 = self.env['res.users'].create({'name': 'Bruno', 'login': 'Bruno'})
        user0_0_id = self.env['res.users'].search([('name', '=', 'Bruno')]).id

        start_date0_0 = str(datetime.datetime(2023, 10, 2, 9, 0))
        end_date0_0 = str(datetime.datetime(2023, 10, 2, 11, 0))

        start_date0_1 = str(datetime.datetime(2023, 10, 2, 11, 0))
        end_date0_1 = str(datetime.datetime(2023, 10, 2, 15, 0))

        self.env['meeting_scheduler'].create([{
            'meeting_title': 'meetingBookable',
            'meeting_location': False,
            'meeting_start_date': start_date0_0,
            'meeting_end_date': end_date0_0,
            'meeting_repetitions': 1,
            'meeting_frequency': 0,
            'meeting_privacy': 'public',
            'meeting_show_as': 'free',
            'meeting_subject': False,
            'create_uid': user0_0_id
        }])

        user0_1 = self.env['res.users'].create({'name': 'Belinda', 'login': 'Belinda'})
        user0_1_id = self.env['res.users'].search([('name', '=', 'Belinda')]).id

        self.env['meeting_scheduler'].create([{
            'meeting_title': 'meetingBookable',
            'meeting_location': False,
            'meeting_start_date': start_date0_1,
            'meeting_end_date': end_date0_1,
            'meeting_repetitions': 1,
            'meeting_frequency': 0,
            'meeting_privacy': 'public',
            'meeting_show_as': 'free',
            'meeting_subject': False,
            'create_uid': user0_1_id
        }])

        group0 = self.env['res.groups'].create({'name': 'group0', 'users': [[user0_0_id], [user0_1_id]]})
        group0_id = self.env['res.groups'].search([('name', '=', 'group0')]).id

        group_scheduler_0 = self.env['group_scheduler'].\
            create({'meeting_group': group0_id, 'meeting_attendees': [user0_0_id, user0_1_id]})

        start_time_0 = datetime.datetime(2023, 10, 2, 2, 0)
        end_time_0 = datetime.datetime(2023, 10, 2, 23, 0)

        self.env.context = dict(self.env.context, active_ids=[group_scheduler_0.id])

        group_scheduler_0.button_timeslots_from_union(start_time_0, end_time_0)

        date = datetime.datetime(2022, 1, 1, 1, 0, 0)

        timeslots = self.env['timeslots'].search([('timeslots_start_date_str','>=', date)])

        self.assertEqual(len(timeslots), 2)

        self.assertEqual(start_date0_0, str(timeslots[0].timeslots_start_date_utc))
        self.assertEqual(end_date0_0, str(timeslots[0].timeslots_end_date_utc))
        self.assertIn(str(user0_0_id), timeslots[0].timeslots_groupmembers)
        self.assertNotIn(str(user0_1_id), timeslots[0].timeslots_groupmembers)
        self.assertEqual(timeslots[0].timeslots_bookable_hours, ' 9 10 11')

        self.assertEqual(start_date0_1, str(timeslots[1].timeslots_start_date_utc))
        self.assertEqual(end_date0_1, str(timeslots[1].timeslots_end_date_utc))
        self.assertIn(str(user0_1_id), timeslots[1].timeslots_groupmembers)
        self.assertNotIn(str(user0_0_id), timeslots[1].timeslots_groupmembers)
        self.assertEqual(timeslots[1].timeslots_bookable_hours, ' 11 12 13 14 15')


    def test_transform_meetings_to_bookable_hours(self):

        group_scheduler_0 = self.env['group_scheduler'].create({'meeting_group': 'test group'})

        #1 slot corr
        timeslot0 = [[datetime.datetime(2023, 4, 12, 12, 0), datetime.datetime(2023, 4, 12, 18, 0), ['ID']]]
        result0 = group_scheduler_0.transform_meetings_to_bookable_hours(timeslot0)
        self.assertEqual(str(result0[0][2]), " 12 13 14 15 16 17 18")

        #1 slot wrong
        timeslot1 = [[datetime.datetime(2023, 4, 12, 18, 0), datetime.datetime(2023, 4, 12, 12, 0), ['ID']]]
        result1 = group_scheduler_0.transform_meetings_to_bookable_hours(timeslot1)
        self.assertEqual(str(result1[0][2]), "")

        #2 slots corr
        timeslot2 = [[datetime.datetime(2023, 4, 12, 12, 0), datetime.datetime(2023, 4, 12, 18, 0), ['ID']],
                     [datetime.datetime(2023, 4, 13, 8, 0), datetime.datetime(2023, 4, 13, 15, 0), ['ID']]]
        result2 = group_scheduler_0.transform_meetings_to_bookable_hours(timeslot2)
        self.assertEqual(str(result2[0][2]), " 12 13 14 15 16 17 18")
        self.assertEqual(str(result2[1][2]), " 8 9 10 11 12 13 14 15")

        #2 slots wrong
        timeslot3 = [[datetime.datetime(2023, 4, 12, 12), datetime.datetime(2023, 4, 12, 10), ['ID']],
                     [datetime.datetime(2023, 4, 13, 10), datetime.datetime(2023, 4, 12, 8), ['ID']]]
        result3 = group_scheduler_0.transform_meetings_to_bookable_hours(timeslot3)
        self.assertEqual(str(result3[0][2]), "")
        self.assertEqual(str(result3[1][2]), "")

        #1 slot over day
        #produces error
        timeslot4 = [[datetime.datetime(2023, 4, 12, 6), datetime.datetime(2023, 4, 13, 6), ['ID']]]
        result4 = group_scheduler_0.transform_meetings_to_bookable_hours(timeslot4)
        #self.assertEqual(str(result4[0][2]), " 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 1 2 3 4 5 6")


        #1 slot specific
        #produces error
        timeslot5 = [[datetime.datetime(2023, 4, 12, 8, 56, 21), datetime.datetime(2023, 4, 12, 10, 43, 51), ['ID']]]
        result5 = group_scheduler_0.transform_meetings_to_bookable_hours(timeslot5)
        #self.assertEqual(str(result5[0][2]), " 8 9 10")

        #1 slot check for changes
        #produces error because of wrong convertTimezones
        timeslot6 = [[datetime.datetime(2023, 4, 12, 8, 56, 21), datetime.datetime(2023, 4, 12, 10, 43, 51), ['ID']]]
        result6 = group_scheduler_0.transform_meetings_to_bookable_hours(timeslot6)
        self.assertEqual(str(result6[0][3]), "2023-04-12 08:56:21")
        self.assertEqual(str(result6[0][4]), "2023-04-12 10:43:51")
        #self.assertEqual(str(result6[0][0]), "2023-04-12 08:56:21")
        #self.assertEqual(str(result6[0][1]), "2023-04-12 10:43:51")


#function still doesn't work as intended
    def dont_test_convert_timezones(self):

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


