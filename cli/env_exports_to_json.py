#!/usr/bin/env python3

"""
Read JSON from file(s) or STDIN, print human-readable format

Options:
    [[FILE] ... ]
        Read JSON from files. If not specified, wait for STDIN
"""
import argparse
import io
import json
import sys
import modules.shell_env_to_json
comment_characters = ['#']


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="Scan shell script(s) or STDIN, and output a JSON blob of all environment variables set.")
    parser.add_argument('file', nargs='*',
                        help="Read env variables from files. If not specified, wait for STDIN")
    parser.add_argument('-c', '--strip-comments', action='store_true',
                        help='Ignore comments in [FILE].')
    parser.add_argument('-p', '--comment_string', type=str, nargs='*',
                        help='Character(s) to indicate a comment.\nThese are in addition to the default \'#\'')
    parser.add_argument('-i', '--indent', type=int, default=4,
                        help="If specified, a prettyprint representation of the JSON will be returned")
    args = parser.parse_args()

    setj = modules.shell_env_to_json.ShellEnvToJSON()

    if len(args.comment_string):
        setj.comment_characters = args.comment_string

    env_dict = dict()
    # Read from STDIN if no file specified
    if len(args.file) == 0:
        env_dict = setj.scan_file(sys.stdin)
    else:
        for f in args.file:
            if not len(env_dict):
                env_dict = setj.scan_file(f)
            else:
                env_dict += setj.scan_file(f)

    print(json.dumps(env_dict, sort_keys=True, indent=args.indent))
