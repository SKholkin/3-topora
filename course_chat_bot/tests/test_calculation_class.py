import unittest
from unittest import mock
from course_chat_bot.calculation_class import Calculations
import datetime
import requests



class TestCalculationClass(unittest.TestCase):

    @mock.patch.object(Calculations, "get_corona_data_by_date",
                       return_value=None)
    def test_get_msg_for_corona(self, mock_var):
        self.assertEqual(type(Calculations.get_msg_for_corona()), str)

    @mock.patch.object(requests, "get",
                       return_value=requests.get(
                           "https://google.com/jhkkhhdfdcgvhbj"))
    def test_get_corona_data_by_date(self, mock_var):
        self.assertEqual(type(Calculations.get_msg_for_corona()), str)

    def test__get_corona_data_by_date_1(self):
        Date = datetime.date(2020, 3, 10)
        self.assertIsNotNone(Calculations.get_corona_data_by_date(Date))

    def test__get_corona_data_by_date_3(self):
        date = datetime.date(2020, 3, 10)
        self.assertIsInstance(Calculations.get_corona_data_by_date(date),
                              requests.Response)

    def test_get_corona_data_by_date_2(self):
        date = datetime.date(2019, 1, 1)
        self.assertRaises(BaseException,
                          Calculations.get_corona_data_by_date(date))

    def test_sort_dictlist_1(self):
        date = datetime.date(2020, 3, 10)
        req = Calculations.get_corona_data_by_date(date)
        self.assertIsInstance(Calculations.sort_corona_dict(req), list)

    def test_sort_dictlist_2(self):
        date = datetime.date(2020, 3, 10)
        req = Calculations.get_corona_data_by_date(date)
        self.assertIsInstance(Calculations.sort_corona_dict(req)[0], dict)

    def test_sum_confirmed_1(self):
        date = datetime.date(2020, 3, 10)
        req = Calculations.get_corona_data_by_date(date)
        self.assertTrue(Calculations.sum_confirmed(req) > 0)

    def test_sum_confirmed_2(self):
        date = datetime.date(2020, 3, 10)
        req = Calculations.get_corona_data_by_date(date)
        self.assertIsInstance(Calculations.sum_confirmed(req), int)

    def test_corona_stats_dynamics_1(self):
        self.assertIsInstance(Calculations.corona_stats_dynamics(), str)

    def test_get_position_weather_1(self):
        self.assertIsInstance(Calculations.get_position_weather(), dict)

    @mock.patch.object(requests, 'get', return_value=requests.get(
        'https://yandex.ru/pogoda/not_url_actually'))
    def test_get_position_weather_2(self, mocked_get):
        self.assertIsNone(Calculations.get_position_weather())

    def test_get_position_weather_3(self):
        self.assertTrue(Calculations.get_position_weather()['position'] >= 0)

    def test_get_weather(self):
        self.assertIsInstance(Calculations.get_weather(), str)

    def test_get_cat_fact_1(self):
        self.assertIsInstance(Calculations.get_cat_fact(), str)

    @mock.patch.object(requests, 'get', return_value=requests.get(
        'https://yandex.ru/pogoda/not_url_actually'))
    def test_get_cat_fact_2(self, mocked_get):
        self.assertIsInstance(Calculations.get_cat_fact(), str)

    @mock.patch.object(requests.Response, 'json', return_value=None)
    def test_fact_parse_1(self, mocked_json):
        r = requests.get('https://cat-fact.herokuapp.com/facts')
        self.assertRaises(BaseException, Calculations.fact_parse(r))

    def test_fact_parse_2(self):
        self.assertRaises(BaseException, Calculations.fact_parse(None))

    def test_fact_parse_3(self):
        r = requests.get('https://cat-fact.herokuapp.com/facts')
        self.assertIsInstance(Calculations.fact_parse(r), str)


if __name__ == '__main__':
    unittest.main()
