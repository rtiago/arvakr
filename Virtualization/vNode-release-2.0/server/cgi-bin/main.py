#!/usr/bin/python

# Copyright (c) Members of the EGEE Collaboration. 2004. 
# See http://www.eu-egee.org/partners/ for details on the copyright
# holders.  
#
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
#
#     http://www.apache.org/licenses/LICENSE-2.0 
#
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.
#
#	vNode Authors:
#		 Ricardo Mendes <Ricardo.Mendes AT cern DOT ch>
#
# vGrid Authors:
#    Omer Khalid <Omer.Khalid AT cern DOT ch>
#    Thomas Koeckerbauer
import cgitb; cgitb.enable()
import os,sys,cgi
os.chdir("..")
sys.path.insert(0, "modules")
import vmstate, time, datetime, re, string, logging, socket, urllib2, re
import configServer, configCommon, pingNode
#, logger
from random import choice

print "Content-type: text/html\n"

#log = logger.getLogger()
username = os.getenv('SSL_CLIENT_S_DN_CN');
try:
  username = "".join([x.strip() for x in username.split(' ')])
except:
  username = 'guest'
form=cgi.FieldStorage();
state = vmstate.VNodeVMState()
vnConfigServer = configServer.getVNodeServerConfig()
vnConfigCommon = configCommon.getVNodeCommonConfig()

proto=vnConfigServer.getProtocol()
path="/cgi/node/cgi-bin/main.py"

def getReservedHostData():
   """ Returns a JSON list with the reserved virtual machines for a given user
   """
   global state
   reservedInfo = []
   logging.info(username + "@" +os.getenv('REMOTE_ADDR') + " is requesting reserved host data")
   reservedNodesHostname = state.getHostsForUserInState(username,'reserved')
   for reservedHostname in reservedNodesHostname:
       reservedNodesInfo = state.getVirtualHostInfo(reservedHostname)
       expiryAtSeconds = reservedNodesInfo['reservedexpirytime']
       if (abs(float(time.time()) - float(expiryAtSeconds)) == 0):
            state.setNotDeployed(reservedHostname)
            break;
       convertExpiryTime = datetime.datetime.fromtimestamp(float(expiryAtSeconds))
       expiryReservedTime = convertExpiryTime.strftime("%H:%M:%S")
       reservedInfo.append({'PhysicalHost':reservedNodesInfo['physicalhost'], 'VirtualHost':reservedHostname,'ExpiryTime':reservedNodesInfo['expirytime'], 'Memory':reservedNodesInfo['vmmemory'], 'Partition':reservedNodesInfo['vmpartition'], 'OSImage':reservedNodesInfo['vmimagetype'], 'ExpiryTimeAt':expiryReservedTime, 'Name':reservedNodesInfo['vmid']})
   print reservedInfo

def getPhysicalHostData():
    """Returns a tuple containing the a list of all available physical host,
    the coloring for them and the defactb-generic-40.cern.ch: 0
ult physical host."""
    physicalHosts = state.getPhysicalHostsBelowMaxVMCountList() 
    physicalHostsColors = {}
    maxVMDict = vnConfigCommon.getPhysicalHostMaxVMDict()
    minFreeSlotRatio = None
    defaultPhysicalHost = None
    for host in physicalHosts:
        logging.info("Host => " + host)
        maxNumOfVMs = eval(maxVMDict.get(host))
        logging.info("Number of max VMs => " + str(maxNumOfVMs))
        numOfVMs = state.getNrOfVMsOnPhysicalHost(host)
        logging.info(numOfVMs)
        freeSlotRatio = numOfVMs / float(maxNumOfVMs)
        logging.info("Free slot ratio => " + str(freeSlotRatio))
        if (minFreeSlotRatio == None) or (freeSlotRatio <= minFreeSlotRatio):
            minFreeSlotRatio = freeSlotRatio
            defaultPhysicalHost = host
    return (physicalHosts, "0", defaultPhysicalHost)

def reserveVM():
  """Reserves a virtual machine for the user. Returns a success exit code if the virtual isn't already in a notDeployed state else returns a failed exit code. 
  """
  vmNodename = form["physicalHost"].value
  vmHostname = form["virtualHostnames"].value
  vmExpiryTime = form["expiryTimeVM"].value
  vmMemory = form["memoryVM"].value
  vmPartition = form["partitionVM"].value
  if not form.has_key("imageFilename"):
    vmOSImage = form["osImageVM"].value
  else:
    vmOSImage = form["imageFilename"].value
  vmName =  vmName = form["vmName"].value
  vmUsername = username
  hostInfo = state.getVirtualHostInfo(vmHostname)
  if hostInfo['state'] != "notDeployed":
    logging.info(username + "@" +os.getenv('REMOTE_ADDR') +" wants to reserve " + vmHostname + " but host is already " + hostInfo['state'])
    print "500"
    return
  logging.info(username + "@" +os.getenv('REMOTE_ADDR') +" is reserving " + vmHostname)
  state.setReserved(vmHostname, vmUsername, vmNodename, vmName, vmOSImage, vmExpiryTime, vmMemory, vmPartition)
  state.setStateMessage(vmHostname, "Reserved");
  print "200"

def deleteReservedVM():
  """ Delete a reserved machine for a user. The virtual machine must be in reserved state and assigned to the user.
  """
  vmHostnames = form["virtualHostnames"].value
  for host in vmHostnames.split(","):
    vmHostData = state.getVirtualHostInfo(host)
    if vmHostData['state'] == 'reserved' and vmHostData['user'] == username:
      logging.info(username + "@" +os.getenv('REMOTE_ADDR') +" is 'deleting' " + host + " from the reserved state")
      state.setNotDeployed(host)
  print "201"
    
def availablePhyHost():
  """ Returns a list with all the available physical hosts in JSON format.
  """
  physicalHosts = []
  physicalHostData = getPhysicalHostData()
  for phyHost in physicalHostData[0]:
    physicalHosts.append({"Physical":phyHost})
  logging.info(username + "@" +os.getenv('REMOTE_ADDR') +" requested available physical hosts => " + str(physicalHosts))
  print {"myData":physicalHosts}
    

def availableHostnames():
  """ Returns a list with all the available hostnames in JSON format.
  """
  virtualHosts = []
  notDeployedHosts = state.getHostsForStateList('notDeployed')
  for host in notDeployedHosts:
    virtualHosts.append({"Hostnames":host})
  logging.info(username + "@" +os.getenv('REMOTE_ADDR') +" requested available Hostnames => " + str(virtualHosts))
  print {"myData":virtualHosts}

def userVM():
  """ Returns a list in JSON format with all the virtual machines in deployed state that belongs to a user.
  """
  global state
  data = []
  logging.info(username + "@" +os.getenv('REMOTE_ADDR') +" is requesting to see what VMs belongs to " + username)
  showTransitionStates = False
  vmHosts = state.getDeployedVirtualHostsInfoDicts(username, getTransitionStates = showTransitionStates)
  for host in vmHosts.keys():
    convertSeconds = datetime.datetime.utcfromtimestamp(abs(float(vmHosts[host]['starttime']) - float(time.time())))
    #upTime = convertSeconds.strftime("%U weeks %H hours %M minutes %S seconds")
    total_seconds = abs(float(vmHosts[host]['starttime']) - float(time.time()))
    # Helper vars:
    MINUTE  = 60
    HOUR = MINUTE * 60
    DAY   = HOUR * 24
    # Get the days, hours, etc:
    days = int( total_seconds / DAY )
    hours   = int( ( total_seconds % DAY ) / HOUR )
    minutes = int( ( total_seconds % HOUR ) / MINUTE )
    seconds = int( total_seconds % MINUTE )
    # Build up the pretty string (like this: "N days, N hours, N minutes, N seconds")
    string = ""
    if days>= 0:
      string += str(days) + " " + (days == 1 and "day" or "days" ) + ", "
    if len(string)>= 0 or hours>= 0:
      string += str(hours) + " " + (hours == 1 and "hour" or "hours" ) + ", "
    if len(string)>= 0 or minutes>= 0:
      string += str(minutes) + " " + (minutes == 1 and "minute" or "minutes" ) + ", "
    string += str(seconds) + " " + (seconds == 1 and "second" or "seconds" )
    upTime=string;
    data.append({'Name':vmHosts[host]['vmid'],'PhysicalHost':vmHosts[host]['physicalhost'], 'VirtualHost':host, 'Uptime':upTime,'OS':vmHosts[host]['vmimagetype']})
  print data

def userVG(sitename):
  """ Returns a list in JSON format with all the virtual machines that belong to a given sitename and username.
      Keyword arguments:
      sitename - If different from 'all' then returns the virtual machines that belong to it. If 'all' returns all the virtual machines from all existing sites
  """
  global state
  data = []
  logging.info(username + "@" +os.getenv('REMOTE_ADDR') +" is requesting to see what VMs belong to a site")
  showTransitionStates = False
  vmHosts = state.getDeployedVirtualHostsInfoDicts(username, getTransitionStates = showTransitionStates)
  for host in vmHosts.keys():
     if sitename == "all":
      if vmHosts[host]['sitename'] != "none":
        data.append({'PhysicalHost':vmHosts[host]['physicalhost'], 'VirtualHost':host})
     else:
      if vmHosts[host]['sitename'] == sitename:
        data.append({'PhysicalHost':vmHosts[host]['physicalhost'], 'VirtualHost':host})
  print data

def upTime():
   """ Returns a list in JSON format with the uptime of all deployed virtual hosts
   """
   global state
   data = []
   logging.info(username + "@" +os.getenv('REMOTE_ADDR') +" is requesting upTime data ")
   vmHosts = state.getDeployedVirtualHostsInfoDicts()
   for host in vmHosts:
      convertSeconds = datetime.datetime.fromtimestamp(abs(float(vmHosts[host]['starttime']) - float(time.time())))
      #upTime = convertSeconds.strftime("%U weeks %H hours %M minutes %S seconds")
      total_seconds = abs(float(vmHosts[host]['starttime']) - float(time.time()))
      # Helper vars:
      MINUTE  = 60
      HOUR = MINUTE * 60
      DAY   = HOUR * 24
      # Get the days, hours, etc:
      days = int( total_seconds / DAY )
      hours   = int( ( total_seconds % DAY ) / HOUR )
      minutes = int( ( total_seconds % HOUR ) / MINUTE )
      seconds = int( total_seconds % MINUTE )
      # Build up the pretty string (like this: "N days, N hours, N minutes, N seconds")
      string = ""
      if days>= 0:
        string += str(days) + " " + (days == 1 and "day" or "days" ) + ", "
      if len(string)>= 0 or hours>= 0:
        string += str(hours) + " " + (hours == 1 and "hour" or "hours" ) + ", "
      if len(string)>= 0 or minutes>= 0:
        string += str(minutes) + " " + (minutes == 1 and "minute" or "minutes" ) + ", "
      string += str(seconds) + " " + (seconds == 1 and "second" or "seconds" )
      upTime=string;
      data.append({'PhysicalHost':vmHosts[host]['physicalhost'], 'VirtualHost':host, 'UpTime':upTime, 'Owner':vmHosts[host]['user']})
   print data

def stateVGData(option):
  """ Returns a list in JSON of virtual machines that are in a given state chosen by the user.
      Keyword arguments:
      option - state of the virtual machines.
  """
  global state
  data = []
  logging.info(username + "@" +os.getenv('REMOTE_ADDR') +" is requesting VG state data with action " + option)
  vmHosts = state.getAllHostsInfoDicts()
  if option == 'all' or option == 'All':
    for host in vmHosts.keys():
      gliteService = ""
      if vmHosts[host]['state'] != 'notDeployed' and vmHosts[host]['state'] != 'disabled':
        if vmHosts[host]['sitename'] != "none":
          if vmHosts[host]['gliteservice_1'] != "none":
            gliteService += vmHosts[host]['gliteservice_1'];
          if vmHosts[host]['gliteservice_2'] != "none":
            gliteService +=' '+vmHosts[host]['gliteservice_2'];
          if vmHosts[host]['gliteservice_3'] != "none":
            gliteService +=' '+vmHosts[host]['gliteservice_3'];
          if vmHosts[host]['gliteservice_4'] != "none":
            gliteService +=' '+vmHosts[host]['gliteservice_4'];
          if vmHosts[host]['gliteservice_5'] != "none":
            gliteService +=' '+vmHosts[host]['gliteservice_5'];
          if len(gliteService) == 0:
            gliteService = "No services defined"
          data.append({'VirtualHost':host,'Owner':vmHosts[host]['user'],'Sitename':vmHosts[host]['sitename'],'StateMessage':vmHosts[host]['state'],'StateColor':vmHosts[host]['state'],'GliteService':gliteService })
  elif option == 'Deployed':
     for host in vmHosts.keys():
      gliteService = ""
      if vmHosts[host]['state'] != 'notDeployed' and vmHosts[host]['state'] != 'disabled':
        if vmHosts[host]['sitename'] != "none" and vmHosts[host]['state'] == "deployed":
          if vmHosts[host]['gliteservice_1'] != "none":
            gliteService += vmHosts[host]['gliteservice_1'];
          if vmHosts[host]['gliteservice_2'] != "none":
            gliteService +=' '+vmHosts[host]['gliteservice_2'];
          if vmHosts[host]['gliteservice_3'] != "none":
            gliteService +=' '+vmHosts[host]['gliteservice_3'];
          if vmHosts[host]['gliteservice_4'] != "none":
            gliteService +=' '+vmHosts[host]['gliteservice_4'];
          if vmHosts[host]['gliteservice_5'] != "none":
            gliteService +=' '+vmHosts[host]['gliteservice_5'];
          if len(gliteService) == 0:
            gliteService = "No services defined"
          data.append({'VirtualHost':host,'Owner':vmHosts[host]['user'],'Sitename':vmHosts[host]['sitename'],'StateMessage':vmHosts[host]['state'],'StateColor':vmHosts[host]['state'],'GliteService':gliteService })
  elif option == 'Failed':
     for host in vmHosts.keys():
      gliteService = ""
      if vmHosts[host]['state'] != 'notDeployed' and vmHosts[host]['state'] != 'disabled':
        if vmHosts[host]['sitename'] != "none" and vmHosts[host]['state'] == "failed":
          if vmHosts[host]['gliteservice_1'] != "none":
            gliteService += vmHosts[host]['gliteservice_1'];
          if vmHosts[host]['gliteservice_2'] != "none":
            gliteService +=' '+vmHosts[host]['gliteservice_2'];
          if vmHosts[host]['gliteservice_3'] != "none":
            gliteService +=' '+vmHosts[host]['gliteservice_3'];
          if vmHosts[host]['gliteservice_4'] != "none":
            gliteService +=' '+vmHosts[host]['gliteservice_4'];
          if vmHosts[host]['gliteservice_5'] != "none":
            gliteService +=' '+vmHosts[host]['gliteservice_5'];
          if len(gliteService) == 0:
            gliteService = "No services defined"
          data.append({'VirtualHost':host,'Owner':vmHosts[host]['user'],'Sitename':vmHosts[host]['sitename'],'StateMessage':vmHosts[host]['state'],'StateColor':vmHosts[host]['state'],'GliteService':gliteService })
  elif option == 'Terminating':
     for host in vmHosts.keys():
      gliteService = ""
      if vmHosts[host]['state'] != 'notDeployed' and vmHosts[host]['state'] != 'disabled':
        if vmHosts[host]['sitename'] != "none" and vmHosts[host]['state'] == "terminating":
          if vmHosts[host]['gliteservice_1'] != "none":
            gliteService += vmHosts[host]['gliteservice_1'];
          if vmHosts[host]['gliteservice_2'] != "none":
            gliteService +=' '+vmHosts[host]['gliteservice_2'];
          if vmHosts[host]['gliteservice_3'] != "none":
            gliteService +=' '+vmHosts[host]['gliteservice_3'];
          if vmHosts[host]['gliteservice_4'] != "none":
            gliteService +=' '+vmHosts[host]['gliteservice_4'];
          if vmHosts[host]['gliteservice_5'] != "none":
            gliteService +=' '+vmHosts[host]['gliteservice_5'];
          if len(gliteService) == 0:
            gliteService = "No services defined"
          data.append({'VirtualHost':host,'Owner':vmHosts[host]['user'],'Sitename':vmHosts[host]['sitename'],'StateMessage':vmHosts[host]['state'],'StateColor':vmHosts[host]['state'],'GliteService':gliteService })
  elif option == 'Deploying':
     for host in vmHosts.keys():
      gliteService = ""
      if vmHosts[host]['state'] != 'notDeployed' and vmHosts[host]['state'] != 'disabled':
        if vmHosts[host]['sitename'] != "none" and vmHosts[host]['state'] == "deploying":
          if vmHosts[host]['gliteservice_1'] != "none":
            gliteService += vmHosts[host]['gliteservice_1'];
          if vmHosts[host]['gliteservice_2'] != "none":
            gliteService +=' '+vmHosts[host]['gliteservice_2'];
          if vmHosts[host]['gliteservice_3'] != "none":
            gliteService +=' '+vmHosts[host]['gliteservice_3'];
          if vmHosts[host]['gliteservice_4'] != "none":
            gliteService +=' '+vmHosts[host]['gliteservice_4'];
          if vmHosts[host]['gliteservice_5'] != "none":
            gliteService +=' '+vmHosts[host]['gliteservice_5'];
          if len(gliteService) == 0:
            gliteService = "No services defined"
          data.append({'VirtualHost':host,'Owner':vmHosts[host]['user'],'Sitename':vmHosts[host]['sitename'],'StateMessage':vmHosts[host]['state'],'StateColor':vmHosts[host]['state'],'GliteService':gliteService })
  print data

def userSiteNames():
   """ Returns a JSON list with all the deployed sitenames that belong to the user
   """
   global state
   data = []
   logging.info(username + "@" +os.getenv('REMOTE_ADDR') +" is requesting all the sitenames that belongs to him")
   vmSitenames = state.getSitenames('deployed',username)
   for site in vmSitenames:
      data.append({"site":site})
   logging.info(username + "@" +os.getenv('REMOTE_ADDR') +" is getting data => " + str(data))
   print {"myData":data}

def terminateVG(option):
  """ Terminate a site that belongs to a user. This function can terminate all the existing user sites      ,terminate a single site or terminate single virtual machines that belong to a site.
      Keyword arguments:
      option - reflects the button that the user clicked.
  """
  if option == "all":
    print "Terminate All VGs"
  elif option == "site":
    vmSite = form["vmSite"].value
    vmHosts = state.getAllHostsInfoDicts()
    for host in vmHosts.keys():
      if vmHosts[host]['state'] != "notDeployed" and vmHosts[host]['state'] != "reserved":
        if (vmHosts[host]['sitename'] == vmSite) and (vmHosts[host]['user'] == username):
          vmPhysicalHost = vmHosts[host]['physicalhost']
          vmName = vmHosts[host]['vmid']
          vmImage = vmHosts[host]['vmimagetype']
          saveImageString = 'no'
          deployNodeAddress = proto + vmPhysicalHost + path + "?&vmAction=remoteTerminate&vmUsername=" + username + "&vmHostname=" + host + "&vmName=" + vmName + "&saveImage=" + saveImageString + "&vmImage=" + vmImage
          logging.info(username + "@" +os.getenv('REMOTE_ADDR') +" is terminating host " + host + " that belongs to a VG")
          urllib2.urlopen(deployNodeAddress).close()
          state.setTerminating(host)
          state.setStateMessage(host, "Sending termination request to node")
    print "203"

def terminateAdmin():
  """ Function used by the administrator of the portal to terminate any virtual machine in any state. 
  """
  vmHostnames = form['virtualHostnames'].value
  #vmUsername = form["username"].value
  for host in vmHostnames.split(","):
    stateDict = state.getVirtualHostInfo(host)
    vmPhysicalHost = stateDict.get('physicalhost')
    vmName = stateDict.get("vmid")
    vmImage = stateDict.get('vmimagetype')
    vmState = stateDict.get('state')
    saveImageString = 'no'
    username_vm = stateDict.get('user')
    if vmState == 'deployed':
      deployNodeAddress = proto + vmPhysicalHost + path + "?&vmAction=remoteTerminate&vmUsername=" + username_vm + "&vmHostname=" + host + "&vmName=" + vmName + "&saveImage=" + saveImageString + "&vmImage=" + vmImage
      logging.info(username + "@" +os.getenv('REMOTE_ADDR') +" is terminating the vm " + host + " that belongs to " + username_vm)
      urllib2.urlopen(deployNodeAddress).close()
      state.setTerminating(host)
      state.setStateMessage(host, "Sending termination request to node")
    elif vmState != 'deploying':
      logging.info(username + "@" +os.getenv('REMOTE_ADDR') +" is terminating the vm " + host + " that belongs to " + username_vm)
      logging.info('vm is not in deployed state so just setting it to notDeployed without contacting node')
      state.setNotDeployed(host)
    else:
      logging.info(username + "@" +os.getenv('REMOTE_ADDR') +" is terminating the vm " + host + " that belongs to " + username_vm)
      logging.info('could not terminate vm!')
  print "204"



def terminateVM():
  """ Function called when user wants to terminate virtual machines
  """
  vmHostnames = form["virtualHostnames"].value
  for host in vmHostnames.split(","):
    stateDict = state.getVirtualHostInfo(host)
    if (stateDict.get('user', None) != username) and (vnConfigServer.getAdministratorsList().count(username) == 0):
      print "202"
      return
    if stateDict.get('state') != "deployed":
      print "202"
      return
    vmPhysicalHost = stateDict.get('physicalhost')
    vmName = stateDict.get("vmid")
    vmImage = stateDict.get('vmimagetype')
    saveImageString = 'no'
    deployNodeAddress = proto + vmPhysicalHost + path + "?&vmAction=remoteTerminate&vmUsername=" + username + "&vmHostname=" + host + "&vmName=" + vmName + "&saveImage=" + saveImageString + "&vmImage=" + vmImage
    logging.info(username + "@" +os.getenv('REMOTE_ADDR') +" is terminating the vm " + host)
    urllib2.urlopen(deployNodeAddress).close()
    state.setTerminating(host)
    state.setStateMessage(host, "Sending termination request to node")
  print deployNodeAddress
 
def deployVG():
  """ Function to deploy a virtual grid. The machines must be in reserved state. If one of the machines is not in reserved state because it expired, this machine will not be deployed but the others virtual machines can still be deployed. To actually deploy the virtual machines this function calls deploy()  
  """
  vmOptions = form["vmOptions"].value
  data = vmOptions.split(",")
  vmSitename = form["vmSitename"].value
  vmRepo = form["vmRepo"].value
  vmGlite = form["vmGlite"].value
  gData = vmGlite.split(",")
  print gData
  gServices = []
  gServicesData = []
  size = len(data)/7
  for i in range(0,size):
    vmHostData = state.getVirtualHostInfo(data[1*size+i])
    if vmHostData['state'] == 'reserved':
      gServicesData.append(data[1*size+i])
      state.setSitename(data[1*size+i],vmSitename) 
      for j in range(0,5):
        gLiteService = gData.pop(0)
        gServicesData.append(gLiteService)
        state.setGliteServiceToReserved(data[1*size+i],data[0*size+i],gLiteService,j)
      gServices = []
  print gServicesData
  logging.info(username + "@" +os.getenv('REMOTE_ADDR') +" is deploying a VG with " + str(vmSitename) + " " + str(vmRepo) + " " + str(gServicesData))
  deploy(vmSitename,vmRepo,gServicesData)
 
def deploy(sitename = "default", repository = "default", vmGliteServices = ['default','none','none','none','none','none']):
  """ Function to deploy a virtual machine. The machines must be in reserved state.  
      Keyword arguments:
      sitename -  If none given it will assume a default value. This happens when not deploying a virtual grid
      repository - default value if not deploying a virtual grid
      vmGliteServices - default value if not deploying a virtual grid
  """
  vmOptions = form["vmOptions"].value
  data = vmOptions.split(",")
  size = len(data)/7
  vmGliteServicesString = string.join(vmGliteServices, ',')
  for i in range(0,size):
    vmHostData = state.getVirtualHostInfo(data[1*size+i])
    if vmHostData['state'] == 'reserved':
      deployNodeAddress = proto + data[0*size+i] + path + "?&vmAction=remoteDeploy&vmUsername=" + username + "&vmName=" + data[6*size+i] + "&vmHostname=" + data[1*size+i] + "&vmMemory=" + data[3*size+i] + "&vmPartition=" + data[4*size+i] + "&vmImage=" + data[5*size+i] + "&vmPhysicalHost=" + data[0*size+i] + "&vmSitename=" + sitename + "&vmRepo=" + repository + "&vmGliteServices=" + vmGliteServicesString
      logging.info(username + "@" +os.getenv('REMOTE_ADDR') +" is going to deploy a virtual machine => " + deployNodeAddress)
      urllib2.urlopen(deployNodeAddress).close()
      state.setDeploying(data[1*size+i],username,data[0*size+i],data[6*size+i],data[5*size+i])
      state.setStateMessage(data[1*size+i], "Sending deployment request to node")
      print deployNodeAddress
 
def getRandomString(length = 13):
   id = ''
   for i in range(length):
      id = id + choice(string.letters)
   return id

#Change this functions to allow clusters (vtb and ctb)
#Needs to be fixed
def autoHosts():
   """ Function to automatically assign reserved hosts to the user
   """
   global state
   nrHosts = form["nrHosts"].value
   logging.info("From " + username + "@" +os.getenv('REMOTE_ADDR') +" got a request to automically choose hosts")
   for i in range(0,int(nrHosts)): 
      notDeployed = state.getHostsForStateList('notDeployed')
      physicalHostData = getPhysicalHostData()
      if (len(physicalHostData) != 0 and len(notDeployed) != 0):
        state.setReserved(notDeployed[0],username,physicalHostData[0][0],getRandomString(),'SLC-4-32','0','256','5')
        state.setStateMessage(notDeployed[0], "Reserved")
   return getReservedHostData()

def stateData(stateRequest):
  """ Function to return a JSON list with virtual machines that are in a given state
      Keyword arguments:
      stateRequest - The state of the virtual machines that will be returned
  """
  global state
  stateData = []
  logging.info("From " + username + "@" +os.getenv('REMOTE_ADDR') +" got a state request for " + stateRequest)
  if stateRequest == 'all':
    deployed = state.getHostsForStateList('deployed')
    respondingHosts = pingNode.pingHosts(deployed)
    notDeployed = state.getHostsForStateList('notDeployed')
    deploying = state.getHostsForStateList('deploying')
    terminating = state.getHostsForStateList('terminating')
    failed = state.getHostsForStateList('failed')
    reserved = state.getHostsForStateList('reserved')
    disabled = state.getHostsForStateList('disabled')
    for host in deployed:
      if (host in respondingHosts):
         stateData.append({'VirtualHost':host,'StateMessage':'deployed','StateColor':'deployed','Message':'Could verify connection to VM'})
      else:
         stateData.append({'VirtualHost':host,'StateMessage':'deployed','StateColor':'deployedNV','Message':'Could not verify connection to VM'})
    for host in notDeployed:
      stateData.append({'VirtualHost':host,'StateMessage':'available','StateColor':'available','Message':'None'})
    for host in reserved:
      nodeInfo = state.getVirtualHostInfo(host)
      userReserve = nodeInfo['user']
      stateData.append({'VirtualHost':host,'StateMessage':'reserved','StateColor':'reserved','Message':'Reserved to '+str(userReserve)})
    for host in failed:
      nodeInfo = state.getVirtualHostInfo(host)
      stateMessage = nodeInfo['statemessage']
      stateData.append({'VirtualHost':host,'StateMessage':'failed','StateColor':'failed','Message':stateMessage})
    for host in terminating:
      nodeInfo = state.getVirtualHostInfo(host)
      stateMessage = nodeInfo['statemessage']
      stateData.append({'VirtualHost':host,'StateMessage':'terminating','StateColor':'terminating','Message':stateMessage})
    for host in deploying:
      nodeInfo = state.getVirtualHostInfo(host)
      stateMessage = nodeInfo['statemessage']
      stateData.append({'VirtualHost':host,'StateMessage':'deploying','StateColor':'deploying','Message':stateMessage})
    print stateData
  elif stateRequest == 'deployed':
    deployed = state.getHostsForStateList('deployed')
    for host in deployed:
      stateData.append({'VirtualHost':host,'StateMessage':'deployed','StateColor':'deployed','Message':'Could verify connection to VM'})
    print stateData
  elif stateRequest == 'deploying':
    deployed = state.getHostsForStateList('deploying')
    for host in deployed:
      nodeInfo = state.getVirtualHostInfo(host)
      stateMessage = nodeInfo['statemessage']
      stateData.append({'VirtualHost':host,'StateMessage':'deploying','StateColor':'deploying','Message':stateMessage})
    print stateData
  elif stateRequest == 'notdeployed':
    deployed = state.getHostsForStateList('notDeployed')
    for host in deployed:
      stateData.append({'VirtualHost':host,'StateMessage':'available','StateColor':'available','Message':'None'})
    print stateData
  elif stateRequest == 'failed':
    deployed = state.getHostsForStateList('failed')
    for host in deployed:
      nodeInfo = state.getVirtualHostInfo(host)
      stateMessage = nodeInfo['statemessage']
      stateData.append({'VirtualHost':host,'StateMessage':'failed','StateColor':'failed','Message':stateMessage})
    print stateData
  elif stateRequest == 'terminating':
    deployed = state.getHostsForStateList('terminating')
    for host in deployed:
      nodeInfo = state.getVirtualHostInfo(host)
      stateMessage = nodeInfo['statemessage']
      stateData.append({'VirtualHost':host,'StateMessage':'terminating','StateColor':'terminating','Message':stateMessage})
    print stateData
  elif stateRequest == 'reserved':
    deployed = state.getHostsForStateList('reserved')
    for host in deployed:
      nodeInfo = state.getVirtualHostInfo(host)
      userReserve = nodeInfo['user']
      stateData.append({'VirtualHost':host,'StateMessage':'reserved','StateColor':'reserved','Message':'Reserved to ' + str(userReserve)})
    print stateData
  elif stateRequest == 'disabled':
    disabled = state.getHostsForStateList('disabled')
    for host in disabled:
      stateData.append({'VirtualHost':host,'StateMessage':'disabled','StateColor':'disabled','Message':'None'})
    print stateData

def disableVM():
  """ Function to disable a virtual machine
  """
  vmHostnames = form["virtualHostnames"].value
  for host in vmHostnames.split(","):
   logging.info("From " + username + "@" +os.getenv('REMOTE_ADDR') +" set " + host + " to disabled")
   state.setDisable(host)
  print "100" 

def enableVM():
  """ Function to enable a virtual machine
  """
  vmHostnames = form["virtualHostnames"].value
  for host in vmHostnames.split(","):
   logging.info("From " + username + "@" +os.getenv('REMOTE_ADDR') +" set " + host + " to notDeployed (enabled)")
   state.setNotDeployed(host)
  print "100"

def disablePortal(stateOpt):
  """ Function to block portal
      Keyword arguments:
      stateOpt - Yes : disable Portal , No : enable Portal
  """
  logging.info("From " + username + "@" +os.getenv('REMOTE_ADDR') +" disable portal is " + stateOpt)
  vnConfigServer.setBlocked(stateOpt)
  print stateOpt

#Re-implement this function
def checkDisablePortal():
  """ Verifies if the portal is disable. Returns a exit code that reflects that
  """
  admins = vnConfigServer.getAdministratorsList()
  res = vnConfigServer.getBlocked()
  logging.info("Portal blocked => " + str(res))
  if username in admins:
    logging.info(str(username) + " is admin")
    if int(res):
      print "920"
    else:
      print "930"
    return
  logging.info(str(username) + " is not admin")
  if int(res):
    print "900"
  else:
    print "910"
  return

def reservedTimeCheck():
  """ Check if a reserved virtual machine hasn't still expired
  """
  hostTime = state.getReservedTimes()
  for i in range(0, len(hostTime)):
    if (re.compile('\D').match(hostTime[i]) == None):
      if ((float(time.time()) - float(hostTime[i])) > 180):
        logging.info("The reserved time for " + hostTime[i-1] + "has expired")
        state.setNotDeployed(hostTime[i-1])
  return

#Security [Implement]
def checkRequestComesFromServer():
  """ Checks the request was actually made from the server
  """
  logging.info("Request comes from " + str(os.getenv('REMOTE_ADDR')))
  return

def getUsername():
  print username
  return

def main():
  checkRequestComesFromServer()
  if form.has_key("vmAction"):
    action = form["vmAction"].value
    logging.info("From " + username + "@" +os.getenv('REMOTE_ADDR') +" got a request with action " + action)
    reservedTimeCheck()
    if action == "reserve": 
      reserveVM()
    elif action == "getReservedData":
      getReservedHostData()
    elif action == "deploy":
      deploy()
    elif action == "deleteReserve":
      deleteReservedVM()
    elif action == "terminateExtra":
      terminateAdmin()
    elif action == "terminate":
      terminateVM()
    elif action == "userVM":
      userVM()
    elif action == "userVG":
      if form.has_key("sitename"):
        userVG(form["sitename"].value);
      else:
        userVG('all'); 
    elif action == "availablePhy":
      availablePhyHost()
    elif action == "availableHostnames":
      availableHostnames()
    elif action == "stateAll":
      stateData('all')
    elif action == "stateDeployed":
      stateData('deployed') 
    elif action == "stateNotDeployed":
      stateData('notdeployed') 
    elif action == "stateFailed":
      stateData('failed') 
    elif action == "stateTerminating":
      stateData('terminating')
    elif action == "stateReserved":
      stateData('reserved')
    elif action == "stateDeploying":
      stateData('deploying')
    elif action == "stateDisabled":
      stateData('disabled')
    elif action == "upTime":
      upTime()
    elif action == "userSiteNames":
      userSiteNames()
    elif action == "autoHosts":
      autoHosts()
    elif action == "deployVG":
      deployVG()
    elif action == "stateVG":
      if form.has_key("vgState"):
        stateVGData(form["vgState"].value)
      else:
        stateVGData('all')
    elif action == "terminateVG":
      terminateVG(form["vmOption"].value)
    elif action == "disableVM":
      disableVM()
    elif action == "enableVM":
      enableVM()
    elif action == "disablePortal":
      disablePortal(form["vmOption"].value)
    elif action == "checkDisablePortal":
      checkDisablePortal()
    elif action == "getUsername":
      getUsername()
    else:
      print "Server Response: Error - What are you trying to do?"
      logging.info("From " + username +"@"+os.getenv('REMOTE_ADDR') + " got a unkown action " + action)

if __name__ == "__main__":
  sys.exit(main())

