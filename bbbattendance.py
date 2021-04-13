#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""bbbattendance.py [-h] [-r ROOM] [-u USER] [-l LOGFILE] [-o OUTFILE.CSV] [date]

This module parses BigBlueButton logs looking for meeting start and stop events
and user join and left events. Can filter events based on date, room name and
user name. Can be run on its own or included in other projects.

It can be used to extract user attendance to meetings, for example for students
attending online classes.

By default it outputs all events occurred from default log file,
`/var/log/bigbluebutton/bbb-web.log`. Since log files are often rotated,
to get data on particular days or meetings you may need to specify a different
file to read.

Dates are formatted in ISO 8601 format (i.e. YYYY-MM-DD, like in 2020-12-31).
Room and user names with spaces should be enclosed in quotes.

Results are put in a CSV file. If no file name is specified by the user, data is
written to a file beginning with `bbb-report` (for example:
`bbb-report-2020-12-31-roomname-username.csv`).
Columns output:
Date,Time,Room,User,Event

Events may be "meeting start", "meeting end", "user join" and "user left".
When meetings end before an user left, no "user left" event is reported.

Note: This program depends on Python 3. If running Python < 3.7 you also need
the `iso8601` module. To install it, use `pip3 install iso8601` or
`apt install python3-iso8601` (on Debian and Ubuntu).
"""

# Copyright 2021 Gerlando Lo Savio
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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

today = dt.date.today().strftime("%Y-%m-%d")

###################################################################
# DEFAULT CONFIGURATION
# This configuration can be overridden by command line arguments
###################################################################
def_logfile = "/var/log/bigbluebutton/bbb-web.log"
def_output_basename = "bbb-report"
# Empty strings for date, room and user mean "any date", "any room" and so on
def_date = ""
def_room = ""
def_user = ""
# Uncomment to use today as default date
#def_date = today


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
    epilog="""Without any option outputs all events occurred from default log
    file. Since log files are often rotated, you may need to specify which
    log file to use.

    Results are put in a CSV file, by default beginning with "bbb-report".
    Columns output: Date,Time,Room,User,Event
    """
    parser = argparse.ArgumentParser(
                description=desc, epilog=epilog)
    parser.add_argument("-d", "--date", type=str, default=date,
                help="date of the events to extract, written like {}".format(today))
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

def read_data(logfile):
    """read_data: Read logfile and collect lines related to meeting start/end and
    user join/left events. Return a list of lines matching the events (or even an
    empty list, if there were no events in the supplied logfile).
    """
    # Regex to match relevant log lines including start, end, join and left events
    pattern = ".*(user_joined_message|user_left_message|meeting_started|meeting_ended).*"
    line_regex = re.compile(pattern)

    # Read lines from log and put matching ones in raw_attendance list
    with open(logfile, "r") as log:
        raw_attendance = []
        for line in log:
            if (line_regex.search(line)):
                raw_attendance.append(line)
    log.close()
    # return a list of strings including the matching lines (or an empty list,
    # if there no start, end, join and left events in the logfile)
    return raw_attendance

def parse_data(raw_attendance):
    """parse_data: Parse each item of raw_attendance, and return a list of dicts
    including: Date, Time, Room, User affected (if applicable) and Event recorded
    """
    ## Event data is in a JSON object. Compile a regular expression to extract it
    pattern = re.compile('data=(.*)')
    parsed_attendance = []
    for line in raw_attendance:
        # extract timestamps
        try:
            timestamp = dt.datetime.fromisoformat(line[0:29])
        except AttributeError:
            # required for python3 < 3.7 compatibility
            timestamp = iso8601.parse_date(line[0:29])
        # We use dates in ISO 8601 format i.e. YYYY-MM-DD
        evdate = timestamp.strftime('%Y-%m-%d')
        evtime = timestamp.strftime('%H:%M')
        # Search and extract json data from line
        payload = pattern.search(line).group(1)
        data = json.loads(payload)
        # get required details for each event
        evroom = data['name']
        event = data['description']
        # get username, of the user joing (or leaving) the meeeting, while
        # meeting start and end events aren't related to any specific user
        if data['logCode'] == "user_joined_message" or data['logCode'] == "user_left_message":
            evuser = data['username']
        elif data['logCode'] == "meeting_started" or data['logCode'] == "meeting_ended":
            evuser = ""

        record = {'Date': evdate, 'Time': evtime, "Room": evroom, "User": evuser, "Event": event}
        parsed_attendance.append(record)

    # return a list of dicts including date, time, room, user (if applicable) and event
    return parsed_attendance

def filter_data(parsed_attendance, req_date='', req_room='', req_user=''):
    """filter_data: Filter data in parsed_attendance, pulling out events related
    to req_date, req_room and req_user, if specified by the user.
    Return a list of dicts like parsed_attendance.
    """
    filtered_attendance = []
    for line in parsed_attendance:
        if req_date == '' or req_date == line['Date']:
            if req_room == '' or req_room == line['Room']:
                if line['Event'] == "Meeting has started." or line['Event'] == "Meeting has ended.":
                    filtered_attendance.append(line)
                elif line['Event'] == "User joined the meeting." or line['Event'] == "User left the meeting.":
                    if req_user == "" or req_user == line['User']:
                        filtered_attendance.append(line)

    # return a list of dicts including date, time, room, user (if applicable) and event
    return filtered_attendance

def save_attendace(filtered_attendance, outfile):
    """save_attendace: Write filtered_attendance data to a CSV file called outfile.
    """
    fieldnames = list(filtered_attendance[0].keys())
    with open(outfile, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for record in filtered_attendance:
            writer.writerow(record)

    csvfile.close()
    print("Data written to {}".format(outfile))


###################################################################
# MAIN
###################################################################
if __name__ == '__main__':
    # Check current python version and requirements
    py_version = sys.version_info
    if py_version[0] != 3:
        print("Sorry, this program requires Python 3")
        sys.exit(1)
    elif py_version[1] < 7:
        # Python < 3.7 doesn't provide datetime.datetime.fromisoformat(),
        # in this case we need the iso8601 module
        try:
            import iso8601
        except:
            print("With Python < 3.7, this program requires  'iso8601' module.")
            print("Please install it with `pip3 install iso8601` or `apt install python3-iso8601`")
            sys.exit(1)

    # Get user input, or use defaults
    req_date, req_room, req_user, logfile, outfile = get_user_input(
                                    def_date, def_room, def_user,
                                    def_logfile, def_output_basename)

    # Read events from logfile. Warn the user if logfile can't be found, or
    # if there are no events to parse and then exit
    try:
        raw_attendance = read_data(logfile)
    except FileNotFoundError:
        print("Sorry, can't find {} - try a different log file!".format(logfile))
        sys.exit(2)
    else:
        if len(raw_attendance) == 0:
            print("Sorry, no events found, try a different log file.")
            sys.exit(3)

    # Parse lines from log file, and convert them in a list of dicts with the data
    parsed_attendance = parse_data(raw_attendance)

    # filter events based on req_date, req_room, and/or req_user
    filtered_attendance = filter_data(parsed_attendance, req_date, req_room, req_user)
    if len(filtered_attendance) == 0:
        print("Sorry, no matching events found, try different parameters or a different log file.")
        sys.exit(4)

    # try to export processed data to outfile, otherwise exits with an error
    try:
        # Save filtered_attendance data to outfile as a CSV file
        save_attendace(filtered_attendance, outfile)
        # TODO: wich exception is raised when we can't write to outfile?
        # can we give more useful directions to users?
    except Exception as ex:
        print("Sorry, can't save attendance to {} \n{}".format(outfile, ex))
        sys.exit(5)
    else:
        # Since everything went fine, return success to the shell
        sys.exit(0)
