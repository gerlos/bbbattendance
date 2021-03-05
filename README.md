# BBBattendance

This program parses **BigBlueButton** logs for a specific date, looking for meeting start and stop events, and user join and left events. Can filter events based on room name and user name. Can be run on its own or included as a module in other projects.

It can be used to extract user attendance to meetings, for example for students attending online classes.

By default it outputs all events occurred in the current day from default log file, `/var/log/bigbluebutton/bbb-web.log`.

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
 $ bbbattendance.py [-h] [-r ROOM] [-u USER] [-l LOGFILE] [-o OUTFILE.CSV] [date]
```

All the arguments and options are optional.

Dates should be formatted in ISO 8601 format (i.e. `YYYY-MM-DD`, like in 2020-12-31). If no date is provided, the current date will be used.

Room and user names with spaces should be in quotes. If no room (or user) is specified, all the rooms (and users) found are reported.

By default it reads default log file, `/var/log/bigbluebutton/bbb-web.log`. Since log files are often rotated, you may need to specify a different file to read.

Results are put in a CSV file. If no file name is specified by the user, data is written to a file beginning with `bbb-report` (for example: `bbb-report-2020-12-31-roomname-username.csv`).

*Note: you should check the exact spelling of the user name, since often guests can choose any name they wish, and typos can happen.*

## Examples

Get attendance for room *"Main Room"* on March the 4th, 2020:

```bash
 $ bbbattendance.py 2020-03-04 -r "Main Room"
```

Get attendance for user John Doe in room *"Main Room"* on March the 4th, 2020:

```bash
 $ bbbattendance.py -r "Main Room" 2020-03-04 -u "John Doe"
```

Get attendance for all the rooms on March the 4th, 2020 from `bbb-web.log`, and write the report to `~/myreport.csv`:

```bash
 $ bbbattendance.py -l bbb-web.log -o ~/myreport.csv 2020-03-04
```


## Requirements

**The script depends on Python 3.** On Python < 3.7 it requires also the `iso8601` module.

To install the `iso8601` module, use `pip3 install iso8601` or `apt install python3-iso8601` (on Debian and Ubuntu).

## Motivation

This program has been written to record student attendance to online classes
at Istituto Tolman, a Psychotherapy school in Italy.
