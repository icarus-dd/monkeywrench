#!/usr/bin/env python3
"""
Functions like the *NIX `tee` command - but does not write to STDOUT unless specified

mw_tee.py [OPTION]... [FILE]...

Options:
       -a, --append
              append to the given FILEs, do not overwrite

       -i, --ignore-interrupts
              ignore interrupt signals
"""
import argparse
import signal
import sys

# Keywords to pass standard I/O as file names in arguments
FILE_STDOUT = '<<STDOUT>>'
FILE_STDERR = '<<STDERR>>'


def get_options():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='Functions like the *NIX `tee` command - but does not write to STDOUT unless specified.',)
    parser.add_argument('-a', '--append', action='store_true',
                        help='append to the given FILEs, do not overwrite.')
    parser.add_argument('-i', '--ignore-interrupts', action='store_true', help='ignore interrupt signals')
    parser.add_argument('file', type=str, nargs='+',
                        help='files to output too.\nThe string literals ' +
                        '%s and %s can be used to output to terminal\n' % (FILE_STDERR, FILE_STDOUT) +
                        'as the standard *NIX tee command does.')

    args = parser.parse_args()
    return args.append, args.ignore_interrupts, args.file


def interrupt_handler():
    pass


if __name__ == "__main__":
    __status_output = True
    __file_mode = 'a'
    __append, __ignore_interrupts, __files = get_options()
    if FILE_STDOUT in __files or FILE_STDERR in __files:
        __status_output = False

    if __ignore_interrupts and __status_output:
        print("Interrupts will be ignored.")
        signal.signal(signal.SIGINT, interrupt_handler)

    if __append and __status_output:
        print('Output files will be appended instead of overwritten')
        __file_mode = 'a'
    else:
        if __status_output:
            print('Output files will be overwritten.')
        __file_mode = 'w'

    __f_handles = []
    for __f in __files:
        if __f == FILE_STDOUT:
            __f_handles.append(sys.stdout)
        elif __f == FILE_STDERR:
            __f_handles.append(sys.stderr)
        else:
            __f_handles.append(open(__f, __file_mode))

    for line in sys.stdin:
        for __f in __f_handles:
            __f.write(line)
