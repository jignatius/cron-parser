#!/usr/bin/env /usr/bin/python3
from io import StringIO
from unittest import TestCase, main
from unittest.mock import patch
from cron_parser.cron_parser import CronParser, NO_EXPRESSION, INVALID_INPUT, INVALID_FORMAT


class TestSum(TestCase):
    def test_empty_string(self):
        parser = CronParser()
        parser.parse("")
        self.assertEqual(parser.error, NO_EXPRESSION)

    def test_bad_input(self):
        parser = CronParser()
        parser.parse(1)
        self.assertEqual(parser.error, INVALID_INPUT)

    def test_wrong_no_parts(self):
        parser = CronParser()
        parser.parse("*/15 0 1,15 * 1-5")
        self.assertEqual(parser.error, INVALID_FORMAT)

    def test_valid_string(self):
        parser = CronParser()
        parser.parse("*/15 0 1,15 * 1-5 /usr/bin/find")
        self.assertEqual(parser.error, None)

    def test_month_string(self):
        parser = CronParser()
        parser.parse("*/15 0 1,15 JAN 1-5 /usr/bin/find")
        self.assertEqual(parser.error, None)

    def test_out_of_range(self):
        parser = CronParser()
        parser.parse("*/15 0 1,15 JAN 1-7 /usr/bin/find")
        self.assertNotEqual(parser.error, None)

    def test_single_value(self):
        parser = CronParser()
        parser.parse("*/15 0 1,15 JAN 1-6 /usr/bin/find")
        self.assertEqual(parser.hour.values, [0])

    def test_interval(self):
        parser = CronParser()
        parser.parse("*/15 0 1,15 JAN 1-6 /usr/bin/find")
        self.assertListEqual(parser.minute.values, [0, 15, 30, 45])

    def test_range(self):
        parser = CronParser()
        parser.parse("*/15 0 1,15 JAN 1-6 /usr/bin/find")
        self.assertListEqual(parser.day_of_week.values, [1, 2, 3, 4, 5, 6])

    def test_all_values(self):
        parser = CronParser()
        parser.parse("*/15 0 1,15 * 1-6 /usr/bin/find")
        self.assertListEqual(parser.month.values, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

    def test_list(self):
        parser = CronParser()
        parser.parse("*/15 0 1,15 JAN 1-6 /usr/bin/find")
        self.assertListEqual(parser.day_of_month.values, [1, 15])

    def test_non_numeric(self):
        parser = CronParser()
        parser.parse("*/15 0 1,15 JAN 1-f /usr/bin/find")
        self.assertNotEqual(parser.error, None)

    def test_valid_string_output(self):
        parser = CronParser()
        parser.parse("*/15 0 1,15 * 1-5 /usr/bin/find")
        with patch('sys.stdout', new=StringIO()) as fake_out:
            parser.output()
            self.assertEqual(fake_out.getvalue(),
                             "minute        0 15 30 45\n"
                             "hour          0\n"
                             "day of month  1 15\n"
                             "month         1 2 3 4 5 6 7 8 9 10 11 12\n"
                             "day of week   1 2 3 4 5\n"
                             "command       /usr/bin/find\n")


if __name__ == '__main__':
    main()
