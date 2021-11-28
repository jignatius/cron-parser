#!/usr/bin/env python3
import sys
from cron_parser.cron_parser import CronParser


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) == 2:
        parser = CronParser()
        if parser.parse(sys.argv[1]):
            parser.output()
        else:
            print(parser.error)
    else:
        print("Invalid number of arguments")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
