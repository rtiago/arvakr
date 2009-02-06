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

import sys, os, logging

def startForked(function, args = [], keywords = {},
                stdout='/dev/null', stderr=None, stdin='/dev/null'):
    """Forks another detached process. The processes are independent so that
    one can exit without influencing the other. The new process starts in the
    specified function which gets passed to specified args and keywords. The
    stdin stdout and stderr are also getting detached from the ones of the
    parent process, the new stdin stdout and stderr files can be specified."""
    # flush to make sure the output does not get duplicated
    sys.stdout.flush()
    sys.stderr.flush()
    # do the UNIX double-fork magic, see Stevens' "Advanced 
    # Programming in the UNIX Environment" for details (ISBN 0201563177)
    pid = os.fork()
    if pid > 0:
        # exit first parent
        return
 
    # decouple from parent environment
    os.chdir("/") 
    os.setsid() 
    os.umask(0)
    # do second fork
    try: 
        pid = os.fork()
        if pid > 0:
            # exit from second parent
            sys.exit(0)
    except SystemExit:
        raise
    except:
        logging.exception("fork #2 failed") 
        sys.exit(1) 
    # Open file descriptors
    if not stderr:
        stderr = stdout
    si = file(stdin, 'r')
    so = file(stdout, 'a+')
    se = file(stderr, 'a+', 0)
    
    # Redirect standard file descriptors.
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno()) 
    # start the forked function
    function(*args, **keywords)
