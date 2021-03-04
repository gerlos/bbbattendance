#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import csv
import json
import re
import sys
import datetime as dt

__author__ = "Gerlando Lo Savio"
__copyright__ = "Copyright 2021 Gerlando Lo Savio"
__license__ = "LGPL"
__date__ = "2021-03-04"
__version__ = 1.3

###################################################################
# DEFAULT CONFIGURATION
# This configuration will be overridden by command line arguments
###################################################################
def_logfile = "/var/log/bigbluebutton/bbb-web.log"
def_output_basename = "bbb-report"
# Default date is today
def_date = dt.date.today().strftime("%Y-%m-%d")
# Empty strings for room and user mean "any room" and "any user"
def_room = ""
def_user = ""

###################################################################
#FUNCTIONS
###################################################################
def gen_outfile_name(req_date, req_room, req_user):
    """gen_outfile_name: Generate a string to use as a file name for the CSV
    report file, based on criteria specified by the user, if any.
    """
    basename = def_output_basename
    ext = ".csv"
    # append user specified criteria to file name
    for item in req_date, req_room, req_user:
        if item != "":
            basename = basename + "-" + item
    filename = basename + ext
    return filename

def get_user_input(date, room, user, logfile, outfile):
    """get_user_input: Read arguments from command line, and set defaults if
    any parameter is missing.
    Returns a list of parameters for subsequent processing.
    """
    desc = """Extract logs start and stop events for rooms and join and left
    events for users from BigBlueButton log. Can filter events based on date,
    room name, and user name.
    """
    epilog="""Without any option outputs all events occurred in the current day
    from default log file. Since log files are often rotated, you may need to
    specify which one to use.

    Results are put in a CSV file, by default beginning with "bbb-report".
    Columns output: Date,Time,Room,User,Event
    """
    parser = argparse.ArgumentParser(
                description=desc, epilog=epilog)
    parser.add_argument("date", type=str, nargs='?', default=date,
                help="date of the events to extract, written like {} (default is today)".format(date))
    parser.add_argument("-r", "--room", type=str, default=room,
                help="room to search for")
    parser.add_argument("-u", "--user", type=str, default=user,
                help="user to search for")
    parser.add_argument("-l", "--logfile", type=str, default=logfile,
                help="log file to parse, default is {}".format(logfile))
    parser.add_argument("-o", "--outfile", type=str, default=outfile,
                help="output file to save parsed data, default is '{}-...'".format(outfile))
    args = parser.parse_args()

    if args.outfile == outfile:
        req_outfile = gen_outfile_name(args.date, args.room, args.user)
        print("User didn't provided any output file name, data will be saved to {}".format(req_outfile))
    else:
        req_outfile = args.outfile

    return args.date, args.room, args.user, args.logfile, req_outfile


###################################################################
# MAIN
###################################################################
if __name__ == '__main__':
    # Check current python version and requirements
    py_version = sys.version_info
    if py_version[0] != 3:
        print("Sorry, this program requires Python 3")
        sys.exit(1)
    
    # Get user input, or use defaults if missing
    req_date, req_room, req_user, logfile, outfile = get_user_input(
                                    def_date, def_room, def_user,
                                    def_logfile, def_output_basename)
