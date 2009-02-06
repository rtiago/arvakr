#!/usr/bin/python

# Copyright (c) Members of the EGEE Collaboration. 2004. 
# See https://www.eu-egee.org/partners/ for details on the copyright
# holders.  
#
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
#
#     https://www.apache.org/licenses/LICENSE-2.0 
#
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.
#
# vNode Authors:
#		 Ricardo Mendes <Ricardo.Mendes AT cern DOT ch>
#
# vGrid Authors:
#    Omer Khalid <Omer.Khalid AT cern DOT ch>
#    Thomas Koeckerbauer

import logging, StringIO, traceback, sys, cgi
from logging.handlers import SysLogHandler

logger = None

def getLogger():
    """Returns the logger singleton instance."""
    global logger
    if logger == None:
        logger = VNodeLogger()
    return logger

class VNodeLogger:
    """vNode logger class for initializing the syslog output and the web output."""
    __webStreamHandler = None

    def __init__(self):
        """Initalize the log handlers."""
        logging.getLogger('').setLevel(logging.DEBUG)
        self.__setupWebOutput()
        self.__setupFileOutput('../logs/vnode-server.log')
        self.__setupSysLogOutput()

    def __setupSysLogOutput(self):
        """Sets up the handler for to the local syslog daemon."""
        syslogHandler = SysLogHandler("/dev/log", SysLogHandler.LOG_DAEMON)
        syslogHandler.setLevel(logging.INFO)
        formatter = logging.Formatter('vNode: %(levelname)s %(funcName)s: %(message)s')
        syslogHandler.setFormatter(formatter)
        logging.getLogger('').addHandler(syslogHandler)

    def __setupFileOutput(self, logFilename):
        """Sets up the logging to a file."""
        try:
            #fileHandler = logging.FileHandler(logFilename)
            fileHandler = logging.handlers.RotatingFileHandler(logFilename,'a',10000000,10)
            fileHandler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s: %(message)s')
            fileHandler.setFormatter(formatter)
            logging.getLogger('').addHandler(fileHandler)
        except:
            logging.exception("Failed to create file logger")

    def __setupWebOutput(self):
        """Sets up the logging to a HTML formated string for web output."""
        VNodeLogger.__webOutput = StringIO.StringIO()
        streamHandler = logging.StreamHandler(VNodeLogger.__webOutput)
        streamHandler.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(levelname)-8s %(message)s<br>')
        streamHandler.setFormatter(formatter)
        logging.getLogger('').addHandler(streamHandler)
        VNodeLogger.__webStreamHandler = streamHandler

    def getWebOutput(self):
        """Returns the HTML formated web output string."""
        return cgi.escape(VNodeLogger.__webOutput.getvalue())
