#!/usr/bin/env python3

"""
Read JSON from file or STDIN, print human-readable format

Options:
    [[FILE] ... ]
        Read JSON from files. If not specified, wait for STDIN
"""
import argparse
import json
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="Read JSON from file or STDIN, print human-readable format")
    parser.add_argument('file', nargs='*',
                        help="Read JSON from files. If not specified, wait for STDIN")
    parser.add_argument('-i', '--indent', type=int, default=4,
                        help="Number of spaces to indent output.")
    parser.add_argument('-m', '--merge', action='store_true',
                        help="Merge contents of multiple files into single JSON blob.\n" +
                        "This also suppresses the filename(s) appearing in the output.")

    args = parser.parse_args()

    if args.merge and len(args.file) == 0:
        print('\n--merge is only valid when reading from files.\n', file=sys.stderr)
        parser.print_help()
        quit(1)

    if len(args.file):
        if args.merge:
            __i = 0
            __json = None
            for __f in args.file:
                with open(__f) as __j:
                    if __i == 0:
                        __json = json.load(__j)
                    else:
                        __json += json.load(__j)

            print(json.dumps(__json, sort_keys=True, indent=args.indent))
        else:
            for __f in args.file:
                print(' >>> ' + __f)
                with open(__f) as __j:
                    print(json.dumps(json.load(__j), sort_keys=True, indent=args.indent))
                    print('\n')

    else:
        print(json.dumps(json.load(sys.stdin), sort_keys=True, indent=args.indent))