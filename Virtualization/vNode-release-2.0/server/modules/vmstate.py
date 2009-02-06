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


import logging, fcntl
from ConfigParser import SafeConfigParser
import configCommon, time

class VNodeVMState:
    __stateFilename = 'state/vnodevmstate.cfg'
    __file = None
    
    def __init__(self):
        self.__state = SafeConfigParser()
        self.__file = open(VNodeVMState.__stateFilename, 'a+')
        self.__file.seek(0)
        fcntl.lockf(self.__file, fcntl.LOCK_EX)
        self.__state.readfp(self.__file)
        self.__initMissingEntriesWithDefaultValues()
    
    def __initMissingEntriesWithDefaultValues(self):
        vnConfig = configCommon.getVNodeCommonConfig()
        virtualHosts = vnConfig.getVirtualHostList()
        for host in virtualHosts:
            if (not self.__state.has_section(host)):
                logging.error('Host "' + host + '" not in state file, adding default value' )
                self.__state.add_section(host)
                self.setNotDeployed(host)

    def __getDict(self, sectionName):
        dict = {}
        items = self.__state.items(sectionName)
        for entry in items:
            dict[entry[0]] = entry[1]
        return dict
    
    def __writeStateFile(self):
        self.__file.seek(0)
        self.__file.truncate()
        self.__state.write(self.__file)
        self.__file.flush()

    def getVirtualHostInfo(self, hostname):
        hostinfo = self.__getDict(hostname)
        return hostinfo
    
    def getDeployedVirtualHostsInfoDicts(self, username = None, vmId = None, getTransitionStates = False):
        hosts = {}
        sections = self.__state.sections()
        for section in sections:
            hostdict = self.__getDict(section)
            if (((hostdict['state'] == 'deployed' and not getTransitionStates ) or
                 (hostdict['state'] != 'notDeployed' and getTransitionStates ))
                and ( username == None or hostdict.get('user', None) == username)
                and ( vmId == None or hostdict.get('vmid', None) == vmId)):
                hosts[section] = hostdict
        return hosts

    def getAllHostsInfoDicts(self):
        hosts = {}
        sections = self.__state.sections()
        for section in sections:
            hosts[section] = self.__getDict(section)
        return hosts

    def setNotDeployed(self, virtualHost):
        self.__state.set(virtualHost, 'state', 'notDeployed')
        if (self.__state.has_option(virtualHost, 'physicalhost')):
            self.__state.remove_option(virtualHost, 'physicalhost')
        if (self.__state.has_option(virtualHost, 'user')):
            self.__state.remove_option(virtualHost, 'user')
        if (self.__state.has_option(virtualHost, 'vmid')):
            self.__state.remove_option(virtualHost, 'vmid')
        if (self.__state.has_option(virtualHost, 'vmimagetype')):
            self.__state.remove_option(virtualHost, 'vmimagetype')
        if (self.__state.has_option(virtualHost, 'statemessage')):
            self.__state.remove_option(virtualHost, 'statemessage')
        if (self.__state.has_option(virtualHost, 'starttime')):
            self.__state.remove_option(virtualHost, 'starttime')
        if (self.__state.has_option(virtualHost, 'failedpings')):
            self.__state.remove_option(virtualHost, 'failedpings')
        if (self.__state.has_option(virtualHost, 'expirytime')):
            self.__state.remove_option(virtualHost, 'expirytime')
        if (self.__state.has_option(virtualHost, 'vmmemory')):
            self.__state.remove_option(virtualHost, 'vmmemory')
        if (self.__state.has_option(virtualHost, 'vmpartition')):
            self.__state.remove_option(virtualHost, 'vmpartition')
        if (self.__state.has_option(virtualHost, 'vmimagetype')):
            self.__state.remove_option(virtualHost, 'vmimagetype')
        if (self.__state.has_option(virtualHost, 'gliteservice_1')):
            self.__state.remove_option(virtualHost, 'gliteservice_1')
        if (self.__state.has_option(virtualHost, 'gliteservice_2')):
            self.__state.remove_option(virtualHost, 'gliteservice_2')
        if (self.__state.has_option(virtualHost, 'gliteservice_3')):
            self.__state.remove_option(virtualHost, 'gliteservice_3')
        if (self.__state.has_option(virtualHost, 'gliteservice_4')):
            self.__state.remove_option(virtualHost, 'gliteservice_4')
        if (self.__state.has_option(virtualHost, 'gliteservice_5')):
            self.__state.remove_option(virtualHost, 'gliteservice_5')
        if (self.__state.has_option(virtualHost, 'reservedexpirytime')):
            self.__state.remove_option(virtualHost, 'reservedexpirytime')
        if (self.__state.has_option(virtualHost, 'sitename')):
            self.__state.remove_option(virtualHost, 'sitename')
        self.__writeStateFile()

    def setDeploying(self, virtualHost, user, physicalHost, vmid, vmImageType):
        self.__state.set(virtualHost, 'physicalhost', physicalHost)
        self.__state.set(virtualHost, 'user', user)
        self.__state.set(virtualHost, 'vmid', vmid)
        self.__state.set(virtualHost, 'vmimagetype', vmImageType)
        self.__state.set(virtualHost, 'state', 'deploying')
        self.__state.set(virtualHost, 'startTime', str(time.time()))
        self.__state.set(virtualHost, 'failedpings', "0")
        if (not self.__state.has_option(virtualHost, 'gliteservice_1')):
            self.__state.set(virtualHost, 'gliteService_1', "none")
        if (not self.__state.has_option(virtualHost, 'gliteservice_2')):
            self.__state.set(virtualHost, 'gliteService_2', "none")
        if (not self.__state.has_option(virtualHost, 'gliteservice_3')):
            self.__state.set(virtualHost, 'gliteService_3', "none")
        if (not self.__state.has_option(virtualHost, 'gliteservice_4')):
            self.__state.set(virtualHost, 'gliteService_4', "none")
        if (not self.__state.has_option(virtualHost, 'gliteservice_5')):
            self.__state.set(virtualHost, 'gliteService_5', "none")
        if (not self.__state.has_option(virtualHost, 'sitename')):
            self.__state.set(virtualHost, 'sitename', "none")
        self.__writeStateFile()

    def setReserved(self, virtualHost, user, physicalHost, vmid, vmImageType, expiryTime, vmMemory, vmPartition):
        self.__state.set(virtualHost, 'physicalhost', physicalHost)
        self.__state.set(virtualHost, 'user', user)
        self.__state.set(virtualHost, 'vmid', vmid)
        self.__state.set(virtualHost, 'vmimagetype', vmImageType)
        self.__state.set(virtualHost, 'state', 'reserved')
        self.__state.set(virtualHost, 'startTime', str(time.time()))
        self.__state.set(virtualHost, 'failedpings', "0")
        self.__state.set(virtualHost, 'expirytime', expiryTime)
        self.__state.set(virtualHost, 'reservedexpirytime', str(time.time() + 60))
        self.__state.set(virtualHost, 'vmmemory', vmMemory)
        self.__state.set(virtualHost, 'vmpartition', vmPartition)
        self.__state.set(virtualHost, 'gliteService_1', "none")
        self.__state.set(virtualHost, 'gliteService_2', "none")
        self.__state.set(virtualHost, 'gliteService_3', "none")
        self.__state.set(virtualHost, 'gliteService_4', "none")
        self.__state.set(virtualHost, 'gliteService_5', "none")
        self.__state.set(virtualHost, 'sitename', "none")
        self.__writeStateFile()

    def setGliteServiceToReserved(self, virtualHost, physicalHost, gService, gIndex):  
        if gIndex == 0:
           self.__state.set(virtualHost, 'gliteService_1', gService)
        if gIndex == 1:
           self.__state.set(virtualHost, 'gliteService_2', gService)
        if gIndex == 2:
           self.__state.set(virtualHost, 'gliteService_3', gService)
        if gIndex == 3:
           self.__state.set(virtualHost, 'gliteService_4', gService)
        if gIndex == 4:
           self.__state.set(virtualHost, 'gliteService_5', gService)
        self.__writeStateFile()

    def setSitename(self, virtualHost, sitename):
        self.__state.set(virtualHost, 'sitename', sitename)
        self.__writeStateFile()

    def removeGliteServices(self, virtualHost, physicalHost):
        if self.__state.get(virtualHost, 'physicalhost') == physicalHost:
           self.__state.set(virtualHost, 'gliteService_1', "none")
           self.__state.set(virtualHost, 'gliteService_2', "none")
           self.__state.set(virtualHost, 'gliteService_3', "none")
           self.__state.set(virtualHost, 'gliteService_4', "none")
           self.__state.set(virtualHost, 'gliteService_5', "none")
        self.__writeStateFile()

    def setFailedPingCount(self, virtualHost, failedPings):
        self.__state.set(virtualHost, 'failedpings', str(failedPings))
        self.__writeStateFile()
        
    def setExpiryTime(self, virtualHost, expiryTime):
        self.__state.set(virtualHost, 'expirytime', str(expiryTime))
        self.__writeStateFile()

    def setStateMessage(self, virtualHost, message):
        self.__state.set(virtualHost, 'statemessage', message)
        self.__writeStateFile()

    def setDeployed(self, virtualHost):
        self.__state.set(virtualHost, 'state', 'deployed')
        if (not self.__state.has_option(virtualHost, 'sitename')):
            self.__state.set(virtualHost, 'sitename', "none")
        if (not self.__state.has_option(virtualHost, 'gliteService_1')):
            self.__state.set(virtualHost, 'gliteService_1', "none")
        if (not self.__state.has_option(virtualHost, 'gliteService_2')):
            self.__state.set(virtualHost, 'gliteService_2', "none")
        if (not self.__state.has_option(virtualHost, 'gliteService_3')):
             self.__state.set(virtualHost, 'gliteService_3', "none")
        if (not self.__state.has_option(virtualHost, 'gliteService_4')):
             self.__state.set(virtualHost, 'gliteService_4', "none")
        if (not self.__state.has_option(virtualHost, 'gliteService_5')):
             self.__state.set(virtualHost, 'gliteService_5', "none")
        if (self.__state.has_option(virtualHost, 'statemessage')):
            self.__state.remove_option(virtualHost, 'statemessage')
        self.__writeStateFile()

    def setTerminating(self, virtualHost):
        self.__state.set(virtualHost, 'state', 'terminating')
        self.__writeStateFile()

    def setDisable(self, virtualHost):
        self.__state.set(virtualHost, 'state', 'disabled')
        self.__writeStateFile()

    def setFailed(self, virtualHost):
        self.__state.set(virtualHost, 'state', 'failed')
        if (not self.__state.has_option(virtualHost, 'gliteService_1')):
          self.__state.set(virtualHost, 'gliteService_1', "none")
        if (not self.__state.has_option(virtualHost, 'gliteService_2')):
          self.__state.set(virtualHost, 'gliteService_2', "none")
        if (not self.__state.has_option(virtualHost, 'gliteService_3')):
          self.__state.set(virtualHost, 'gliteService_3', "none")
        if (not self.__state.has_option(virtualHost, 'gliteService_4')):
          self.__state.set(virtualHost, 'gliteService_4', "none")
        if (not self.__state.has_option(virtualHost, 'gliteService_5')):
          self.__state.set(virtualHost, 'gliteService_5', "none")
        if (not self.__state.has_option(virtualHost, 'sitename')):
          self.__state.set(virtualHost, 'sitename', "none")
        self.__writeStateFile()

    def getHostsForStateList(self, state):
        hostlist = []
        hosts = self.__state.sections()
        for host in hosts:
            if (self.__state.get(host, 'state') == state):
                hostlist.append(host)
        return hostlist

    def getHostsForSitename(self, user, state, sitename):
        hostlist = []
        hosts = self.__state.sections()
        for host in hosts:
            if (self.__state.get(host, 'state') == state and 
                self.__state.get(host, 'user') == user and self.__state.get(host, 'sitename') == sitename):
                hostlist.append(host)
        return hostlist

    def getHostsForUserInState(self, user, state):
        hostlist = []
        hosts = self.__state.sections()
        for host in hosts:
            if (self.__state.get(host, 'state') == state and 
                self.__state.get(host, 'user') == user):
                hostlist.append(host)
        return hostlist

    def getAllSitenames(self):
        sitesnameslist = []
        unorderedSitesnames = []
        hosts = self.__state.sections()
        for host in hosts:
            if (self.__state.get(host, 'state') != 'notDeployed' and self.__state.get(host, 'state') != 'reserved' and self.__state.get(host, 'sitename') != 'none'):
                unorderedSitesnames.append(self.__state.get(host,'sitename'))
        for x in unorderedSitesnames:
            if x not in sitesnameslist:
               sitesnameslist.append(x)
        return sitesnameslist

    def getReservedTimes(self):
        timeList = []
        hosts = self.__state.sections()
        for host in hosts:
            if (self.__state.get(host, 'state') == 'reserved'):
              timeList.append(host)
              timeList.append(self.__state.get(host, 'starttime'))
        return timeList
    
    def getSitenames(self,state,user):
        sitesnameslist = []
        unorderedSitesnames = []
        hosts = self.__state.sections()
        for host in hosts:
            if user == 'all':
               if (self.__state.get(host, 'state') == state and self.__state.get(host, 'sitename') != 'none'):
                  unorderedSitesnames.append(self.__state.get(host,'sitename'))
            else:
               if (self.__state.get(host, 'state') == state and self.__state.get(host, 'sitename') != 'none' and self.__state.get(host,'user') == user):
                  unorderedSitesnames.append(self.__state.get(host,'sitename'))

        for x in unorderedSitesnames:
            if x not in sitesnameslist:
               sitesnameslist.append(x)
        return sitesnameslist

    def getSiteInfoFromSitename(self, sitenames, user):
        siteInfo = []
        hosts = self.__state.sections()
        for sitename in sitenames:
           siteInfo.append(sitename)
           tempSiteInfo = []
           for host in hosts:
             if user == 'all':
                if (self.__state.get(host, 'state') != 'notDeployed' and self.__state.get(host,'state') != 'reserved' and self.__state.get(host, 'sitename') == sitename):
                   tempSiteInfo.append(host)
                   tempUser = self.__state.get(host, 'user')
             else:
                if (self.__state.get(host, 'state') != 'notDeployed' and self.__state.get(host, 'sitename') == sitename and self.__state.get(host,'state') != 'reserved' and self.__state.get(host, 'user') == user):
                   tempSiteInfo.append(host)
                   tempUser = self.__state.get(host, 'user') 
           siteInfo.append(tempUser)
           siteInfo.append(tempSiteInfo)
        return siteInfo

    def getSelectedGliteServices(self, hostnames, state):
        GliteServicesForHost = []
        for host in hostnames:
            if (self.__state.get(host,'state') == state):
                GliteServicesForHost.append(host)
                gliteServices = []
                if (self.__state.get(host, 'gliteservice_1') != 'none'):
                  gliteServices.append(self.__state.get(host, 'gliteservice_1'))
                if (self.__state.get(host, 'gliteservice_2') != 'none'):
                  gliteServices.append(self.__state.get(host, 'gliteservice_2'))
                if (self.__state.get(host, 'gliteservice_3') != 'none'):
                  gliteServices.append(self.__state.get(host, 'gliteservice_3'))
                if (self.__state.get(host, 'gliteservice_4') != 'none'):
                  gliteServices.append(self.__state.get(host, 'gliteservice_4'))
                if (self.__state.get(host, 'gliteservice_5') != 'none'):
                  gliteServices.append(self.__state.get(host, 'gliteservice_5'))
                GliteServicesForHost.append(gliteServices)
        return GliteServicesForHost

    def getGliteServices(self):
        HostsGliteServices = []
        hosts =  self.__state.sections() 
        for host in hosts:
            if (self.__state.get(host, 'state') != 'notDeployed'):
              HostsGliteServices.append(host)
              gliteServices = []
              if (self.__state.get(host, 'gliteservice_1') != 'none'):
                  gliteServices.append(self.__state.get(host, 'gliteservice_1'))
              if (self.__state.get(host, 'gliteservice_2') != 'none'):
                  gliteServices.append(self.__state.get(host, 'gliteservice_2'))
              if (self.__state.get(host, 'gliteservice_3') != 'none'):
                  gliteServices.append(self.__state.get(host, 'gliteservice_3'))
              if (self.__state.get(host, 'gliteservice_4') != 'none'):
                  gliteServices.append(self.__state.get(host, 'gliteservice_4'))
              if (self.__state.get(host, 'gliteservice_5') != 'none'):
                  gliteServices.append(self.__state.get(host, 'gliteservice_5'))
              HostsGliteServices.append(gliteServices)
        return HostsGliteServices

    def getNrOfVMsOnPhysicalHost(self, hostname):
        count = 0
        sections = self.__state.sections()
        for section in sections:
            hostdict = self.__getDict(section)
            if (hostdict['state'] != 'notDeployed' and hostdict['state'] != 'disabled'
                and hostdict['physicalhost'] == hostname):
                count = count + 1
        return count

    def getPhysicalHostsBelowMaxVMCountList(self):
        hosts = []
        vnConfigCommon = configCommon.getVNodeCommonConfig()
        maxVMs = vnConfigCommon.getPhysicalHostMaxVMDict()
        allHosts = vnConfigCommon.getPhysicalHostList()
        for host in allHosts:
            if (self.getNrOfVMsOnPhysicalHost(host) < eval(maxVMs[host])):
                hosts.append(host)
        hosts.sort()
        return hosts
