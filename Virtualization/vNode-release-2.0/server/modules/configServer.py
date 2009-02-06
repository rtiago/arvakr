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
#
# vNode Authors:
#    Ricardo Mendes <Ricardo.Mendes AT cern DOT ch>
#
#
# vGrid Authors:
#    Omer Khalid <Omer.Khalid AT cern DOT ch>
#    Thomas Koeckerbauer

from ConfigParser import SafeConfigParser
import logging, fcntl

ConfigFilePath = "configuration/"

vnConfigServerInstance = None

def getVNodeServerConfig():
  global vnConfigServerInstance
  if vnConfigServerInstance == None:
    vnConfigServerInstance = VNodeServerConfig()
  return vnConfigServerInstance

class VNodeServerConfig:
  
  def __init__(self):
    try:
      self.__configServer = SafeConfigParser()
      self.__file = open(ConfigFilePath + "server.cfg",'a+')
      self.__file.seek(0)
      fcntl.lockf(self.__file, fcntl.LOCK_EX)
      self.__configServer.readfp(self.__file)
    except:
      logging.exception("Config Server file could not be loaded")
    
  def __writeConfigServerFile(self):
    self.__file.seek(0)
    self.__file.truncate()
    self.__configServer.write(self.__file)
    self.__file.flush()

  def __getList(self, sectionName):
    list = []
    try:
      items = self.__configServer.items(sectionName)
      for entry in items:
        list.append(entry[1])
      list.sort()
    except:
      logging.exception("Error parsing configuration file server.cfg")
    return list

  def getBlocked(self):
    return self.__configServer.get("General","blocked")

  def setBlocked(self,val):
    self.__configServer.set("General","blocked",val)
    self.__writeConfigServerFile()

  def getAdministratorsList(self):
    return self.__getList("Administrators")

  def getProtocol(self):
    return self.__configServer.get("General","protocol")

  def getMails(self):
    return self.__configServer.get("General","warningMails")

  def getAdminMail(self):
    return self.__configServer.get("General","adminMail")
 
  
