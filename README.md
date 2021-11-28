# cron-parser

This is a simple cron expression parser written in Python3.

The parser only considers the standard cron format with five time fields (minute, hour, day of month, month, and day of
week) plus a command. It does not handle the special time strings such as "@yearly". The input will be on a single line.

## Installation
```bash
git clone https://github.com/jignatius/cron-parser.git
```

## Usage
The parser is ready to run from the command line on a Linux system with Python 3.6 or higher installed.
Ensure that cron-parser.py is an executable file by running
```bash
chmod +x cron-parser.py
```
Then simply invoke it by calling the script with a cron string like this:
```bash
~$ ./cron-parser.py ＂*/15 0 1,15 * 1-5 /usr/bin/find＂
```
and it should print the following output:
```bash
minute        0 15 30 45
hour          0
day of month  1 15
month         1 2 3 4 5 6 7 8 9 10 11 12
day of week   1 2 3 4 5
command       /usr/bin/find
```
