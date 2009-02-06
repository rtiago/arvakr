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
# vNode Author:
#		 Ricardo Tiago <Ricardo.Mendes AT cern DOT ch>
#
# vGrid Authors:		 
#    Omer Khalid <Omer.Khalid AT cern DOT ch>
#    Thomas Koeckerbauer
import cgitb; cgitb.enable()
from string import Template
import socket, logging, sys, os, cgi
os.chdir("../")
sys.path.insert(0,"modules")
import vmstate, random, time, datetime, configServer

print "Content-type: text/html\n"

state = None
status=cgi.FieldStorage()
vnConfigServer = configServer.getVNodeServerConfig()

def setState():
  """Function to set the deployment status sent by the node
  """
  newState = status["state"].value
  logging.info("Received state from " + os.getenv('REMOTE_ADDR') + " with value " + newState )
  vmHostname = status["vmHostname"].value
  physicalHost = state.getVirtualHostInfo(vmHostname).get('physicalhost', None)
  user = state.getVirtualHostInfo(vmHostname).get('user', None)
  message = state.getVirtualHostInfo(vmHostname).get('statemessage', None)
  convertTime = datetime.datetime.fromtimestamp(time.time())
  dateMailToday = datetime.date.today()
  dateMail = dateMailToday.isoformat()
  timeMail = convertTime.strftime("%H:%M:%S")
  if newState == 'deployed':
    state.setDeployed(vmHostname)
  elif newState == 'notDeployed':
    state.setNotDeployed(vmHostname)
  elif newState == 'failed':
    if int(vnConfigServer.getMails()):
      mailFile=open('tmpl/mail.tmpl','a+')
      data = mailFile.read()
      mailFile.close()
      mailData = dict(virtualmachine=vmHostname,physicalmachine=physicalHost,date=dateMail+' '+timeMail,user=user,status=newState,msg=message)
      s = Template(data).substitute(mailData)
      tmpfile =  'tmp' + str(random.randint(0,10000000))  + vmHostname
      tmpFile=open(tmpfile,'w')
      tmpFile.write(s)
      tmpFile.close()
      os.system('mail -s "vNode Status Message ' + newState + '" ' + vnConfigServer.getAdminMail() + ' < ' + tmpfile)
      os.system('rm ' + tmpfile)
      state.setFailed(vmHostname)
    else:
      state.setFailed(vmHostname)
  else:
    raise Exception("Invalid state: " + str(newState))

def setStateMessage():
  """Function to set the state Message sent by the node
  """
  message = status["stateMessage"].value
  vmHostname = status["vmHostname"].value
  state.setStateMessage(vmHostname,message)

def checkRequestComesFromRightHost(remoteAddress):
  """Verifies that the request came from the right Node
      Keyword arguments:
      remoteAddress -- remote address of the host that sent the request
  """
  vmHostname = status["vmHostname"].value
  physicalHost = state.getVirtualHostInfo(vmHostname).get('physicalhost', None)
  if physicalHost == None:
    raise Exception("No physical host stored for the virtual host")
  if socket.getaddrinfo(remoteAddress, None) != socket.getaddrinfo(physicalHost, None):
    raise Exception("Request was not sent from the node stored in the state file for this virtual host")


def main(remoteAddress):
  """ Main function
      Keyword arguments:
      remoteAddress -- remote address of the host that sent the request
  """
  global state
  state = vmstate.VNodeVMState()
  if status.has_key("vmAction"):
    serverAction = status["vmAction"].value
    if serverAction == "setstate":
      #checkRequestComesFromRightHost(remoteAddress)
      setState()
    elif serverAction == "setstatemessage":
      #checkRequestComesFromRightHost(remoteAddress)
      setStateMessage()
    else:
      print "Received an unknown remote request"
  else:
    print "Received an invalid remote request"


if __name__ == "__main__":
  sys.exit(main(os.getenv('REMOTE_ADDR')))
      
