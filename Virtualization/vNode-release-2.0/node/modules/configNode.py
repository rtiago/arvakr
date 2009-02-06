#!/usr/bin/python
#
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
#   Ricardo Mendes <Ricardo DOT Mendes AT cern DOT ch>
#
#	vGrid Authors:
#		Omar Khalid <Omer.Khalid AT cern DOT ch>
#		Thomas Koechkerbauer
#
#

from ConfigParser import SafeConfigParser
from string import Template
import logging, fcntl, socket, os, string

ConfigFilePath = "configuration/"
vnConfigNodeInstance = None

def getVNodeNodeConfig():
  global vnConfigNodeInstance
  if vnConfigNodeInstance == None:
    vnConfigNodeInstance = VNodeNodeConfig()
  return vnConfigNodeInstance

class VNodeNodeConfig:
	
  def __init__(self):
    try:
      self.__configNode = SafeConfigParser()
      self.__file = open(ConfigFilePath + "node.cfg", "a+")
      self.__file.seek(0)
      fcntl.lockf(self.__file,fcntl.LOCK_EX)
      self.__configNode.readfp(self.__file)
    except:
      logging.exception("node.cfg file could not be loaded")

  def __getDict(self,sectionName):
    dict = {}
    try:
      items = self.__configNode.items(sectionName)
      for entry in items:
        dict[entry[0]] = entry[1]
    except:
      logging.exception("Error parsing node.cfg file")
    return dict

  def __getDictValue(self, sectionName, key, allowDefault = True):
    dict = self.__getDict(sectionName)
    value = dict.get(key.lower(), None)
    if (value == None) and allowDefault:
      value = dict.get('default', None)
    return value

  def getServerHostname(self):
    return self.__configNode.get("General","serverHostname")

  def getVMImageFile(self, vmImage):
    logging.info(vmImage)
    return self.__configNode.get("VMImageFiles",vmImage)

  def getImageDirectory(self):
    return self.__configNode.get("General","imageDirectory")

  def getProtocol(self):
    return self.__configNode.get("General","protocol")

  def getVolumeGroupName(self):
    return self.__configNode.get("General","volumeGroupName")	

  def getVMSwapSize(self, imageType):
    return self.__getDictValue("VMSwapSize", imageType)

  def getXenDeployerFSCreateCmd(self, imageType):
    logging.info(imageType)
    return self.__getDictValue("XenDeployerFSCreateCmd",imageType)
	
  def getVMType(self, imageTag):
    return self.__getDictValue("VMTypes",imageTag)

  #Put this on the configuration file
  def createVMConfigFile(self, username, machinename, vmNodename, vmHostname, vmId, vmMemory, vmPartition, vmImageType, configFilename = None):
    try:
      configFile=open('tmpl/xen.tmpl', 'a+')
      data = configFile.read()
      configFile.close()
      num = os.sysconf('SC_NPROCESSORS_ONLN')
      if vmImageType == "SL-3-32":
        d = dict(machinename=machinename,ip=socket.gethostbyname(vmHostname),hostname=vmHostname,memory=vmMemory,vg='vg1',driveroot='sda1',driveswap='sda2',vcpus=num,username=username)
      else:
        d = dict(machinename=machinename,ip=socket.gethostbyname(vmHostname),hostname=vmHostname,memory=vmMemory,vg='vg1',driveroot='xvda1',driveswap='xvda2',vcpus=num,username=username)
      s = Template(data).substitute(d)
      configFile=open(configFilename,'w')
      configFile.write(s)
      configFile.close()
    except:
      logging.exception("Error creating configuration file for virtual machine")
      raise

  #This can be improved to be more efficient
  def createVMYaimgenFile(self,sitename,repository,username,vmGliteServices):
    count = -1
    try:
      configFile=open('tmpl/yaimgen.tmpl','a+')
      data = configFile.read()
      configFile.close()
      logging.info(vmGliteServices)
      hostdata = []
      vmGliteServices=vmGliteServices.rsplit(',')
      for i in range(0, len(vmGliteServices)):
        if i == 0:
          count+=1
          hostdata.append("ygHOST_" + str(count) + "=" + "\"" + vmGliteServices[i] + " ")
        elif i % 6 == 0:
          count+=1
          hostdata.append("\"" + "\n" + "ygHOST_" + str(count) + "=" + "\"" + vmGliteServices[i] + " ")
        elif (vmGliteServices[i] != "none"):
          hostdata.append(" " + vmGliteServices[i])
      hostdata.append("\"" + "\n")
      d = dict(sitename=sitename,repo=repository,host_data=string.join(hostdata,''))
      s = Template(data).substitute(d)
      configFile=open("yaim/yaimgen_" + sitename + "_vNode.cfg",'w')
      configFile.write(s)
      configFile.close()
    except:
      logging.exception("Error on creating yaimgen configuration file")
      raise 
