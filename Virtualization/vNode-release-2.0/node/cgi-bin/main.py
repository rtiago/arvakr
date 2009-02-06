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
#	vNode Authors:
#		 Ricardo Mendes <Ricardo.Mendes AT cern DOT ch>
#
# vGridAuthors:
#    Omer Khalid <Omer.Khalid AT cern DOT ch>
#    Thomas Koeckerbauer
import cgitb; cgitb.enable()
import socket, os, sys, cgi, urllib2, logging
os.chdir("..")
sys.path.insert(0,"modules")
import configNode, deployer, forkworker
#, logger

print "Content-type: text/html\n"

#log = logger.getLogger()
remoteData=cgi.FieldStorage()
vnConfigNode = configNode.getVNodeNodeConfig()

path="/cgi/server/cgi-bin/status.py"
proto=vnConfigNode.getProtocol()

def reportState(vmHostname, state , serverHostname=None):
  """Reports the current state to Server
      Keyword arguments:
      vmHostname -- Hostname of the virtual machine
      state -- state of the virtual machine
  """
  if serverHostname == None: 
    serverHostname = vnConfigNode.getServerHostname()
  logging.info("sending the state " + state + " to " + serverHostname)
  logging.info(proto + serverHostname + path + "?vmAction=setstate&vmHostname=" + vmHostname + "&state=" + state)
  addr = proto + serverHostname + path + "?vmAction=setstate&vmHostname=" + vmHostname + "&state=" + state
  urllib2.urlopen(addr).close()

def reportStateMessage(vmHostname, message, serverHostname=None):
  """Sends a state message to the Server
      Keyword arguments:
      vmHostname -- Hostname of the virtual machine
      message -- message to be sent
  """
  if serverHostname == None: 
    serverHostname = vnConfigNode.getServerHostname()
  message = message.replace(' ', '%20')
  logging.info("sending a state message " + message + " to " + serverHostname)
  logging.info(proto + serverHostname + path + "?vmAction=setstatemessage&vmHostname=" + vmHostname + "&stateMessage=" + message)
  urllib2.urlopen(proto + serverHostname + path + "?vmAction=setstatemessage&vmHostname=" + vmHostname + "&stateMessage=" + message).close()

def terminate():
  """Function to process the request of the Server to terminate a virtual machine.
  """
  logging.info("terminating a machine for " + str(os.getenv('REMOTE_ADDR')))
  if (not remoteData.has_key("vmHostname")):
    logging.info("No key vmHostname")
    raise Exception('No key vmHostname')
  else:
    vmHostname = remoteData["vmHostname"].value; 
  try:
    vmUsername = remoteData["vmUsername"].value;
    vmName = remoteData["vmName"].value;
    saveImage = remoteData["saveImage"].value;
    machinename = vmUsername + '_' + vmHostname
    vmImage = remoteData["vmImage"].value;
    vmImageType = vmImage
    vgDeployer = deployer.VNodeDeployer.getDeployerForImage(vmImageType)
    vmImageFilename = None
    logging.info("Terminate details for:  " + str(os.getenv('REMOTE_ADDR')))
    logging.info("Username:" + vmUsername)
    logging.info("Name:" + vmName)
    logging.info("Save Image:" + saveImage)
    logging.info("Machine Nname:" + vmUsername + '_' + vmHostname)
    logging.info("Image:" + vmImage)
    logging.info("ImageType:" + vmImageType)
    if (saveImage == 'yes'):
       imageDir = vnConfigNode.getImageDirectory()
       vmImageFilename = imageDir + vmUsername + '_' + vmName + ".tar.gz"
    logging.info("Destroying the virtual machine")
    vgDeployer.destroyVirtualMachine(vmHostname, machinename, vmImageFilename)
  except SystemExit:
  #  raise Exception('Raised by sys.exit()')
     pass
  except:
    forkworker.startForked(reportStateMessage, args=[vmHostname, str(sys.exc_info()[1])])
    forkworker.startForked(reportState , args=[vmHostname, 'failed'])
    logging.info("Could not terminate the virtual machine")
    raise Exception('Could not terminate the virtual machine')

def deploy():
  """Function to process the request of the Server to deploy a virtual machine.
  """
  logging.info("deploying a machine for " + str(os.getenv('REMOTE_ADDR')))
  if (not remoteData.has_key("vmHostname")):
    logging.info("No key vmHostname")
    raise Exception('No vmHostname key')
  else:
    vmHostname = remoteData["vmHostname"].value; 
  try:
    vmUsername = remoteData["vmUsername"].value;
    vmName = remoteData["vmName"].value;
    vmPhysicalHost = remoteData["vmPhysicalHost"].value;
    vmMemory = remoteData["vmMemory"].value;
    vmPartition = remoteData["vmPartition"].value;
    vmSitename = remoteData["vmSitename"].value;
    vmRepo = remoteData["vmRepo"].value;
    vmGliteServices = remoteData["vmGliteServices"].value;
    imageDir = vnConfigNode.getImageDirectory()
    vmImage = remoteData["vmImage"].value;
    imageFilename = vnConfigNode.getVMImageFile(vmImage)
    logging.info("Deploying details for " + str(os.getenv('REMOTE_ADDR')))
    logging.info("Username:" + vmUsername)
    logging.info("Name:" + vmName)
    logging.info("PhysicalHost:" + vmPhysicalHost)
    logging.info("Memory:" + vmMemory)
    logging.info("Partition:" + vmPartition)
    logging.info("Sitename:" + vmSitename)
    logging.info("Repo:" + vmRepo)
    logging.info("Glite Services" + vmGliteServices)
    logging.info("Image:" + vmImage)
    logging.info("Image Filename:" + str(imageFilename))
    if (imageFilename == None and len(vmImage) != 0):
      imageFilename = vmImage
    elif (imageFilename == None and len(vmImage) == 0):
      logging.info("No was image defined")
      raise Exception('No Image')
    vmImageType = vmImage
    if (not imageFilename.startswith('/')):
      imageFilename = imageDir + imageFilename
    logging.info("Image Filename with append path:" + imageFilename)
    if (not os.path.exists(imageFilename)):
      logging.info("Cannot find path to image")
      raise Exception('Cannot find path to image')
    machinename = vmUsername + '_' + vmHostname
    configFilename = "/tmp/vnode_" + machinename + ".cfg"
    vgDeployer = deployer.VNodeDeployer.getDeployerForImage(vmImageType)
    logging.info("Verifying if physical host has enough resources to deploy the machine")
    vgDeployer.checkAvailability(vmMemory, vmPartition, vmImageType)
    logging.info("Creating the configuration file")
    vnConfigNode.createVMConfigFile(vmUsername, machinename, vmPhysicalHost, vmHostname, vmName, vmMemory, vmPartition, vmImageType, configFilename)
    logging.info("Creating the yaimgen configuration file")
    vnConfigNode.createVMYaimgenFile(vmSitename,vmRepo,vmUsername,vmGliteServices)
    logging.info("Creating the virtual machine with the previous defined parameters")
    vgDeployer.createVirtualMachine(configFilename, vmHostname, machinename, imageFilename, vmPartition, vmImageType, vmSitename)
  except SystemExit:
    #raise Exception('Raised by sys.exit()')\
    pass
  except:
    forkworker.startForked(reportStateMessage, args=[vmHostname, str(sys.exc_info()[1])])
    forkworker.startForked(reportState , args=[vmHostname, 'failed'])
    logging.info('Could not deploy the virtual machine')
    raise Exception('Could not deploy the virtual machine')

def checkRequestComesFromServer(remoteAddress):
  """Verifies that the request came from the server
      Keyword arguments:
      remoteAddress -- remote address of the host that sent the request
  """
  serverHostPort = vnConfigNode.getServerHostname()
  serverHostname = serverHostPort.split(':')[0]
  if socket.getaddrinfo(remoteAddress,None) != socket.getaddrinfo(serverHostname, None):
    logging.info("request denied from " + str(remoteAddress) + "<- This is a unkown IP")
    raise Exception('Request denied - [no permissions]')
 
def main(remoteAddress):
  """ Main function
      Keyword arguments:
      remoteAddress -- remote address of the host that sent the request
  """
  try:
    if remoteData.has_key("vmAction"):
      remoteAction = remoteData["vmAction"].value
      logging.info("received a request from " + str(os.getenv('REMOTE_ADDR')) + " with remote action " + remoteAction)
      if remoteAction == "remoteDeploy":
        checkRequestComesFromServer(remoteAddress)
        deploy()
      elif remoteAction == "remoteTerminate":
        checkRequestComesFromServer(remoteAddress)
        terminate()
      else:
        logging.info("received a unkown request from " + str(os.getenv('REMOTE_ADDR')))
    else:
      logging.info("received a invalid request from " + str(os.getenv('REMOTE_ADDR'))) 
  except:
    logging.info('Exception raised')
    if (not remoteData.has_key("vmHostname")):
      logging.info("No key vmHostname")
    else:
      vmHostname = remoteData["vmHostname"].value;
      forkworker.startForked(reportStateMessage, args=[vmHostname, str(sys.exc_info()[1]),os.getenv('REMOTE_ADDR')])
      forkworker.startForked(reportState , args=[vmHostname, 'failed',os.getenv('REMOTE_ADDR')])
   
if __name__ == "__main__":
  sys.exit(main(os.getenv('REMOTE_ADDR')))
