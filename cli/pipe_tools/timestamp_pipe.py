#!/usr/bin/env python3

"""
Command line tool to read STDIN from pipe, output each line prepended with a timestamp.

Options:
    --ampm
            Display timestamps in 12-hour format with AM/PM
    --time-format <format_string>
            format string to pass to the python datetime module

    Note: --ampm and --time-format are mutually exclusive
"""
import argparse
import datetime
import select
import sys

config = {
    'time_format': '[%d/%m/%y %H:%M:%S] ',  # See also get_options() for a second assignment
}


def get_options():
    global config

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="Prepend the current timestamp to every line read from STDIN.\nPrint results to STDOUT.",
        epilog='Note: --ampm and --time-format are mutually exclusive')
    parser.add_argument('-t', '--time-format', type=str,
                        help="format string to pass to the python datetime module." +
                             "\nSee https://docs.python.org/3/library/datetime.html#format-codes"
                        )
    parser.add_argument('--ampm', action='store_true',
                        help='show 12 hour clock with AM/PM')

    # Are we a pipe?
    if not select.select([sys.stdin, ], [], [], 0.0)[0]:
        print("\nERROR\n    No data to pipe.\n", file=sys.stderr)
        parser.print_help()
        quit(1)

    args = parser.parse_args()

    if args.time_format is not None and args.no_ampm:
        print("\nERROR\n    --time-format and --no-ampm are mutually exclusive.\n")
        parser.print_help()
        quit(1)

    if args.time_format is not None:
        config['time_format'] = args.time_format

    if args.ampm:
        config['time_format'] = '[%d/%m/%y %I:%M:%S %p] '


def piper():
    global config
    for line in sys.stdin:
        line = line.rstrip()
        print(datetime.datetime.now().strftime(config['time_format']) + line)


if __name__ == "__main__":
    get_options()
    piper()
