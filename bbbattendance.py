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


###################################################################
# MAIN
###################################################################
if __name__ == '__main__':
    pass
    
