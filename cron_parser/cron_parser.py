from cron_parser.cron_field import Minute, Hour, DayOfMonth, Month, DayOfWeek

NO_EXPRESSION = "No expression!"
INVALID_INPUT = "Invalid argument"
INVALID_FORMAT = "Invalid format"
VALID_NO_PARTS = 6


class CronParser:
    """
    Class for parsing a cron expression.
    """
    def __init__(self):
        self.error = None
        self.command = None
        self.minute = Minute()
        self.hour = Hour()
        self.day_of_month = DayOfMonth()
        self.month = Month()
        self.day_of_week = DayOfWeek()

    def parse(self, expression):
        """
        Parse the given cron expression string.
        :param expression: expression string
        :return: True/False to indicate success/failure
        """
        result = False
        try:
            # empty expression
            if not expression:
                self.error = NO_EXPRESSION
            # not a string
            elif type(expression) != str:
                self.error = INVALID_INPUT
            # string
            else:
                parts = expression.strip().split()
                # wrong number of parts
                if len(parts) != VALID_NO_PARTS:
                    self.error = INVALID_FORMAT
                else:
                    # right number of parts
                    self.command = parts[-1]
                    # parse individual parts
                    self.minute.parse(parts[0])
                    self.hour.parse(parts[1])
                    self.day_of_month.parse(parts[2])
                    self.month.parse(parts[3])
                    self.day_of_week.parse(parts[4])
                    result = True
        except Exception as e:
            self.error = str(e)
        return result

    def output(self):
        """
        Print output.
        :return:
        """
        self.minute.output()
        self.hour.output()
        self.day_of_month.output()
        self.month.output()
        self.day_of_week.output()
        print(f'{"command":<14}{self.command}')

