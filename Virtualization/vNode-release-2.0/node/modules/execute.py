#!/usr/bin/python

# Copyright (c) Members of the EGEE Collaboration. 2004. 
# See httpss://www.eu-egee.org/partners/ for details on the copyright
# holders.  
#
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
#
#     httpss://www.apache.org/licenses/LICENSE-2.0 
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

import logging, os, sys
import subprocess # Python >= 2.4

#Implement a queue mechanism 
def osExecute(cmd):
    """Executed the command specified and returns the exitcode. Note: If the
    command is not found no exception will be raised, instead an exitcode will
    be set."""
    retry = 0
    retcode = 99
    logging.info("Executing '" + cmd + "'")
    try:
      while (retcode != 0 and retry < 5):
        run = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out, err = [ e.splitlines() for e in run.communicate() ]
        logging.info(run.returncode)
        retcode = run.returncode 
        retry = retry + 1
    except:
      logging.info("Could not execute" + cmd + " with retry at " + str(retry) )
      return
    if retry >= 5:
      logging.info("Could not execute" + cmd + " with retry at " + str(retry) + "(should be 5)")
    
def getCommandOutput(cmd):
    lines = []
    try:
        if subprocess: # Python >= 2.4
          proc = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE, stderr=open('/dev/null','w'))
          procOutput = proc.stdout
          print procOutput
        else: # Python 2.3 fallback
            procOutput = os.popen4(cmd)[1]
        while True:
            line = procOutput.readline()
            if not line: break
            lines.append(line)
    except:
        logging.exception("Execution failed for" + cmd)
    return lines


