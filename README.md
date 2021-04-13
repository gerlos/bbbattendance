# BBBattendance

<<<<<<< HEAD
This program parses **BigBlueButton** logs for a specific date, looking for meeting start and stop events, and user join and left events. Can filter events based on room name and user name. It can be run on its own or included as a module in other projects.
=======
This program parses **BigBlueButton** logs looking for meeting start and stop events, and user join and left events. Can filter events based on date, room name and user name. Can be run on its own or included as a module in other projects.
>>>>>>> development

It can be used to extract user attendance to meetings, for example for students attending online classes.

By default it outputs all events found in default log file, `/var/log/bigbluebutton/bbb-web.log`.

Results are put in a CSV file that can be then opened in LibreOffice Calc for further processing.

**Output sample:**

| Date       | Time  | Room      | User          | Event                    |
|------------|-------|-----------|---------------|--------------------------|
| 2021-03-05 | 11:25 | Classroom |               | Meeting has started.     |
| 2021-03-05 | 11:26 | Classroom | Paolo Rossi   | User joined the meeting. |
| 2021-03-05 | 11:27 | Classroom | Laura Bianchi | User joined the meeting. |
| 2021-03-05 | 11:27 | Classroom | Marta Verdi   | User joined the meeting. |
| 2021-03-05 | 12:20 | Classroom | Marta Verdi   | User left the meeting.   |
| 2021-03-05 | 12:20 | Classroom | Paolo Rossi   | User left the meeting.   |
| 2021-03-05 | 12:32 | Classroom |               | Meeting has ended.       |

Events may be `meeting start`, `meeting end`, `user join` and `user left`.
When meetings end before a specific user left, no `user left` event is reported for that user.


## Install

Download, fork or copy paste the script to your machine and make it executable.

```bash
 $ chmod +x bbbattendance.py
```

## Usage

```bash
<<<<<<< HEAD
 $ ./bbbattendance.py [-h] [-r ROOM] [-u USER] [-l LOGFILE] [-o OUTFILE.CSV] [date]
=======
 $ ./bbbattendance.py --help
usage: bbbattendance.py [-h] [-d DATE] [-r ROOM] [-u USER] [-l LOGFILE] [-o OUTFILE]

Extract logs start and stop events for rooms and join and left events for users
from BigBlueButton log. Can filter events based on date, room name, and user name.

optional arguments:
  -h, --help            show this help message and exit
  -d DATE, --date DATE  date of the events to extract, written like 2021-04-13
  -r ROOM, --room ROOM  room to search for
  -u USER, --user USER  user to search for
  -l LOGFILE, --logfile LOGFILE
                        log file to parse, default is /var/log/bigbluebutton/bbb-web.log
  -o OUTFILE, --outfile OUTFILE
                        output file to save parsed data, default is 'bbb-report-...'

Without any option outputs all events occurred from default log file. Since log
files are often rotated, you may need to specify which log file to use. Results
are put in a CSV file, by default beginning with "bbb-report". Columns output:
Date,Time,Room,User,Event
>>>>>>> development
```

All the options are optional.

Dates should be formatted in ISO 8601 format (i.e. `YYYY-MM-DD`, like in 2020-12-31).

Room and user names with spaces should be in quotes. If no date, room or user is specified, events from all the dates, rooms and users found in log file are reported.

By default it reads default log file, `/var/log/bigbluebutton/bbb-web.log`. Since log files are often rotated, you may need to specify a different file to read.

Results are put in a CSV file. If no file name is specified by the user, data is written to a file beginning with `bbb-report` (for example: `bbb-report-2020-12-31-roomname-username.csv`).

*Note: you should check the exact spelling of the user name, since often guests can choose any name they wish, and typos can happen.*

## Examples

Get attendance for room *"Main Room"* on March the 4th, 2020:

```bash
<<<<<<< HEAD
 $ ./bbbattendance.py 2020-03-04 -r "Main Room"
=======
 $ bbbattendance.py --date 2020-03-04 --room "Main Room"
>>>>>>> development
```

Get attendance for user John Doe in room *"Main Room"* on March the 4th, 2020:

```bash
<<<<<<< HEAD
 $ ./bbbattendance.py -r "Main Room" 2020-03-04 -u "John Doe"
=======
 $ bbbattendance.py -u "John Doe" -r "Main Room" -d 2020-03-04
>>>>>>> development
```

Get attendance for all the rooms on March the 4th, 2020 from `bbb-web.log`, and write the report to `~/myreport.csv`:

```bash
<<<<<<< HEAD
 $ ./bbbattendance.py -l bbb-web.log -o ~/myreport.csv 2020-03-04
=======
 $ bbbattendance.py -d 2020-03-04 -l bbb-web.log -o ~/myreport.csv
>>>>>>> development
```


## Requirements

**The script depends on Python 3.** On Python < 3.7 it requires also the `iso8601` module.

To install the `iso8601` module, use either `pip3 install iso8601` or `apt install python3-iso8601` (on Debian, Ubuntu and derivatives).

## Motivation

This program has been written to record student attendance to online classes
at Istituto Tolman, a Psychotherapy school in Italy.
