# Constants
Months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
Weekdays = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']


def _to_num(value):
    """
    Convert string to num.
    :param value: value string
    :return: number
    """
    try:
        num = int(value)
    except ValueError as exc:
        raise ValueError(f'Invalid value {value}')
    return num


def _filter_by_step(values, step):
    """
    Taking a list of values, filter it by step.
    :param values: list of values
    :param step: step value
    :return:
    """
    if step:
        interval_values = []
        pos = 0
        while pos < len(values):
            interval_values.append(values[pos])
            pos += step
        values[:] = interval_values


class Field:
    """
    Base class for cron field.
    """
    def __init__(self, name, min_value, max_value, alternative_names):
        self.name = name
        self.min = min_value
        self.max = max_value
        self.alternative_names = alternative_names
        self.values = None

    def parse(self, expression):
        """
        Parse the given expression string and store the possible values.
        :param expression: expression string
        :return:
        """
        # look for increment first
        parts = expression.split('/')
        step = 0
        if len(parts) > 2:
            raise ValueError(f"Invalid expression: {expression}")
        elif len(parts) == 2:
            step = int(parts[1])
        start = parts[0]

        # all values
        if start == '*':
            self.values = list(range(self.min, self.max+1))
        # letters only
        elif start.isalpha():
            self.values = self._get_alternative_values(start)
        else:
            self.values = self._parse_ranges(start, step)

        _filter_by_step(self.values, step)  # filter values by step

    def _get_alternative_values(self, value_str):
        """
        Taking an alternative name value, convert it to numerical value.
        :param value_str: alternative string value
        :return: numerical value
        """
        idx = self.alternative_names.index(value_str)
        value = self.min + idx
        return value

    def _parse_ranges(self, expression, step):
        """
        Parse the given range and return list of all possible values.
        :param expression: expression string
        :param step: step interval
        :return: list of possible values
        """
        range_set = set()

        if not step:  # no step defined
            # split by ',' first
            for part in expression.split(','):
                # split by '-' next
                sub_parts = part.split('-')
                if len(sub_parts) == 1:
                    if step == 0:
                        range_set.add(_to_num(part))
                    else:
                        self.add_range_values(range_set, _to_num(expression), self.max, expression)
                else:
                    if len(sub_parts) == 2:
                        self.add_range_values(range_set, _to_num(sub_parts[0]), _to_num(sub_parts[1]), expression)
                    else:
                        raise ValueError(f'Invalid expression: {part}')
        else:
            # step defined - so all values starting from numerical value of expression
            self.add_range_values(range_set, _to_num(expression), self.max, expression)

        return list(range_set)

    def add_range_values(self, range_set, min_value, max_value, expression):
        """
        Add all possible values within range to a given set.
        :param range_set: set of values
        :param min_value: minimum value
        :param max_value: maximum value
        :param expression: expression string
        :return:
        """
        self._check_within_range(min_value, max_value, expression)
        range_set.update(int_value for int_value in range(min_value, max_value + 1))

    def _check_within_range(self, min_value, max_value, expression):
        """
        Check minimum and maximum values fall within acceptable range.
        :param min_value: minimum value
        :param max_value: maximum value
        :param expression: expression string
        :return:
        """
        if min_value < self.min or max_value > self.max:
            raise ValueError(f'Invalid range: {expression}')

    def output(self):
        print(f'{self.name:<14}{" ".join(str(x) for x in self.values)}')


class Minute(Field):
    """
    Class for minute field.
    """
    def __init__(self):
        super().__init__('minute', 0, 59, [])


class Hour(Field):
    """
    Class for hour field.
    """
    def __init__(self):
        super().__init__('hour', 0, 23, [])


class DayOfMonth(Field):
    """
    Class for day of month field.
    """
    def __init__(self):
        super().__init__('day of month', 1, 31, [])


class Month(Field):
    """
    Class for month field.
    """
    def __init__(self):
        super().__init__('month', 1, 12, Months)


class DayOfWeek(Field):
    """
    Class for day of week field.
    """
    def __init__(self):
        super().__init__('day of week', 0, 6, Weekdays)
