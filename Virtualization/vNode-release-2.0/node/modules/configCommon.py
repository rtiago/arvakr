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

vnConfigCommonInstance = None

def getVNodeCommonConfig():
  global vnConfigCommonInstance
  if vnConfigCommonInstance == None:
    vnConfigCommonInstance = VNodeCommonConfig()
  return vnConfigCommonInstance

class VNodeCommonConfig:

  def __init__(self):
    try:
      self.__configCommon = SafeConfigParser()
      self.__file = open(ConfigFilePath + "common.cfg", "a+")
      self.__file.seek(0)
      fcntl.lockf(self.__file, fcntl.LOCK_EX)
      self.__configCommon.readfp(self.__file)
    except:
      logging.exception("Config Common file could not be loaded")

  def __writeConfigServerFile(self):
    self.__file.seek(0)
    self.__file.truncate()
    self.__configCommon.write(self.__file)
    self.__file.flush()
 
  def __getDict(self,sectionName):
    dict = {}
    try:
      items = self.__configCommon.items(sectionName)
      for entry in items:
        dict[entry[0]] = entry[1]
    except:
      logging.exception("Error parsing common file")
    return dict

  def getVirtualHostList(self):
    hosts = self.__getDict("VirtualHostsPool").keys()
    hosts.sort()
    return hosts

  def getPhysicalHostList(self):
    hosts = self.__getDict("PhysicalHostsPool").keys()
    hosts.sort()
    return hosts 

  def getPhysicalHostMaxVMDict(self):
    return self.__getDict("PhysicalHostsPool")
	
