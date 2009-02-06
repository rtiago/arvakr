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
#
# vGrid Authors:
#    Omer Khalid <Omer.Khalid AT cern DOT ch>
#    Thomas Koeckerbauer

import cgitb; cgitb.enable()
import logging, execute, os, re, urllib2, forkworker, configNode, popen2, string, sys, libvirt, subprocess


class VNodeXenDeployer:
    def __init__(self):
        self.__config = configNode.getVNodeNodeConfig()
        self.__vgName = self.__config.getVolumeGroupName()
        self.__protocol = self.__config.getProtocol()

    def createVirtualMachine(self, configFile, vmHostname, machinename, imagename, partitionSize, imageType, sitename):
        forkworker.startForked(VNodeXenDeployer.__createVirtualMachine,
                              args=[self, configFile, vmHostname, machinename, imagename, partitionSize, imageType, sitename])

    def destroyVirtualMachine(self, vmHostname, machinename, imagename = None):
        forkworker.startForked(VNodeXenDeployer.__destroyVirtualMachine,
                               args=[self, vmHostname, machinename, imagename])
       
    def checkAvailability(self, vmMemory, vmPartition, imageType):
        #TODO check if enough memory is available
        swapSize = self.__config.getVMSwapSize(imageType)
        if (self.getFreeDiskSpace() < (float(vmPartition)*1024 + float(swapSize))):
            raise Exception('Not enough space on disk left, space left: ' + freeSpace[0] + 'G')        

    def getFreeDiskSpace(self):
        checkPartCmd = "sudo vgs -o vg_free --units M --noheadings " + self.__vgName
        lines = execute.getCommandOutput(checkPartCmd)
        if len(lines) == 0:
            raise Exception('Did not get output from "' + checkPartCmd + '"')
        checkSizeRe = re.compile(r"([\d]+[.\d]*)M")
        freeSpace = re.findall(checkSizeRe, lines[0])
        if not freeSpace:
            raise Exception('Could not parse output from "' + checkPartCmd + '"')
        return float(freeSpace[0])

    def __reportState(self, vmHostname, state):
        serverHostname = self.__config.getServerHostname()
        urllib2.urlopen(self.__protocol + serverHostname + "/cgi/server/cgi-bin/status.py?vmAction=setstate&vmHostname=" + vmHostname + "&state="+ state).close()

    def __reportStateMessage(self, vmHostname, message):
        serverHostname = self.__config.getServerHostname()
        message = message.replace(' ', '%20')
        logging.info(self.__protocol + serverHostname + "/cgi/server/cgi-bin/status.py?vmAction=setstatemessage&vmHostname=" + vmHostname + "&stateMessage="+ message)
        urllib2.urlopen(self.__protocol + serverHostname + "/cgi/server/cgi-bin/status.py?vmAction=setstatemessage&vmHostname=" + vmHostname + "&stateMessage="+ message).close()

    def __createVirtualMachine(self, configFile, vmHostname, machinename, imagename, partitionSize, imageType, sitename):
        logging.info('creating virtual machine')
        tempMountpoint = "/tmp/vnode_" + machinename
        mkfsCommand = self.__config.getXenDeployerFSCreateCmd(imageType)
        if (mkfsCommand == None):
            raise Exception('no mkfs command specified')
        try:
            self.__reportStateMessage(vmHostname, "Creating LVM partitions")
            self.__createLVMPartition(machinename, partitionSize, mkfsCommand, imageType)
            try: 
                self.__createMountpoint(machinename, tempMountpoint)
                self.__reportStateMessage(vmHostname, "Uncompressing image")
                self.__untarimage(imagename, tempMountpoint)
                self.__reportStateMessage(vmHostname, "Configuring yaimgen")
                self.__getYaim(machinename, tempMountpoint, sitename)
            except:
                self.__removeMountpoint(tempMountpoint)
                raise
            self.__removeMountpoint(tempMountpoint)
            try:
                self.__reportStateMessage(vmHostname, "Starting virtual machine")
                self.__startVirtualMachine(machinename, configFile)
                if self.__getDomainId(machinename) == -1:
                    self.__reportState(vmHostname, 'failed')
                else:
                    self.__reportState(vmHostname, 'deployed')
            except:
                self.__shutdownVirtualMachine(machinename)
                raise
        except:
            self.__removeLVMPartition(machinename)
            self.__reportState(vmHostname, 'failed')
            return

    def __destroyVirtualMachine(self, vmHostname, machinename, imagename):
        logging.info('removing virtual machine')
        try:
            self.__reportStateMessage(vmHostname, "Shutting down virtual machine")
            self.__shutdownVirtualMachine(machinename)
            if (imagename != None):
                self.__reportStateMessage(vmHostname, "Saving image")
                self.__saveImage(machinename, imagename)
            self.__reportStateMessage(vmHostname, "Removing LVM partitions")
            self.__removeLVMPartition(machinename)
            self.__reportState(vmHostname, 'notDeployed')
        except:
            self.__reportState(vmHostname, 'failed')
        logging.info('virtual machine removed')

    def __getDomainId(self, machinename):
        conn = libvirt.openReadOnly(None)
        if conn == None:
            raise Exception('Failed to open connection to the hypervisor')
        try:
            return conn.lookupByName(machinename).ID()
        except:
            logging.info('No VM "' + machinename + '" running')
            return -1

    def __getYaim(self, machinename, tempMountpoint, sitename):
        yaimFile = "/usr/local/vnode-2.0/yaim/yaimgen_" + sitename + "_vNode.cfg"
        moveYaimFile = "sudo cp " + yaimFile + " " +  tempMountpoint + "/root/yaimgen/"
        logging.info(moveYaimFile)
        try:
           output = execute.getCommandOutput(moveYaimFile)
        except:
          logging.info('cannot get yaimgen configuration')
          raise 

    def __shutdownVirtualMachine(self, machinename):
        logging.info('shutting down virtual machine')
        
        configFile = "/etc/xen/auto/vnode_" + machinename + ".cfg"
        removeConfigFile = "sudo rm -f " + configFile
        try:
            #domainId = self.__getDomainId(machinename)
            #if domainId != -1:
            #  shutdown = "sudo xm destroy " + str(domainId)
            shutdown = "sudo xm destroy " + machinename
            execute.osExecute(shutdown)
        except:
            logging.info('cannot shutdown "' + machinename + '"')
            execute.osExecute(removeConfigFile)
            raise
        execute.osExecute(removeConfigFile)

    def __startVirtualMachine(self, machinename, configFile):
        logging.info('starting the virtual machine')
        newConfigFile = "/etc/xen/auto/vnode_" + machinename + ".cfg" 
        moveConfigFile = "sudo mv " + configFile + " " + newConfigFile
        startup = "sudo xm create -f " + newConfigFile
        try:
            execute.osExecute(moveConfigFile)
            execute.osExecute(startup)
        except:
            logging.info('cannot start the domain with config file: ' + configFile)
            raise

    def __untarimage(self, imagename, destDir):
        logging.info("Untar image")
        untarimage = "sudo tar -zxvf " + imagename + " -C " + destDir

        try:
            execute.osExecute(untarimage)
        except:
            logging.info('Failed to uncompress image')
            raise

    def __saveImage(self, machinename, imagename):
        tempMountpoint = "/tmp/vnode_" + machinename

        tarimage = "sudo tar -cszvf " + imagename + " -C "  + tempMountpoint + " ."
        
        try:
            self.__createMountpoint(machinename, tempMountpoint)
            execute.osExecute(tarimage)
        except:
            logging.info('failed in saving the image -> ' + imagename)
            self.__removeMountpoint(tempMountpoint)
            raise
        self.__removeMountpoint(tempMountpoint)
    
    def __createLVMPartition(self, machinename, partitionSize, mkfsCommand, imageType):
        try:
            swapSize = self.__config.getVMSwapSize(imageType)
            lvrootcreate = "sudo lvcreate --size " + partitionSize + "G --name xen-root-" + machinename + " " + self.__vgName
            lvswapcreate = "sudo lvcreate --size " + swapSize + "M --name xen-swap-" + machinename + " " + self.__vgName
            makeswap = "sudo mkswap /dev/" + self.__vgName + "/xen-swap-" + machinename
            filesystem = "sudo " + mkfsCommand + " /dev/" + self.__vgName + "/xen-root-" + machinename
            execute.osExecute(lvrootcreate)
            execute.osExecute(lvswapcreate)
            execute.osExecute(filesystem)
            execute.osExecute(makeswap)
        except:
            logging.info("Failed to create LVM partition")
            raise

    def __checkPartitionExists(self, partitionName):
        getPartCmd = "sudo lvs -o lv_name,lv_size|grep " + partitionName
        lines = execute.getCommandOutput(getPartCmd)
        return len(lines) > 0

    def __removeLVMPartition(self, machinename):
        rootPartName = "xen-root-" + machinename
        swapPartName = "xen-swap-" + machinename
        lvrootremove = "sudo lvremove -f /dev/" + self.__vgName + "/" + rootPartName
        lvswapremove = "sudo lvremove -f /dev/" + self.__vgName + "/" + swapPartName
        
        try:
            try:
                if self.__checkPartitionExists(rootPartName):
                    execute.osExecute(lvrootremove)
            except:
                logging.info('LVM Root Partition /dev/' + self.__vgName + '/xen-root-' + machinename + ' is NOT removed')
                raise
        finally:
            try:
                if self.__checkPartitionExists(swapPartName):
                    execute.osExecute(lvswapremove)
            except:
                logging.info('LVM Swap Partition /dev/' + self.__vgName + '/xen-swap-' + machinename + ' is NOT removed')
                raise
    
    def __createMountpoint(self, machinename, mountpoint):
        logging.info('creating mount point')

        mountlvm = "sudo mount /dev/" + self.__vgName + "/xen-root-" + machinename + " " + mountpoint

        try:
            os.mkdir(mountpoint)
            execute.osExecute(mountlvm)
            os.chdir(mountpoint)
        except:
            logging.info('Failed to mount vm root partition')
            raise

    def __removeMountpoint(self, mountpoint):
        logging.info('removing mount point')
        unmountlvm = "sudo umount " + mountpoint

        try:
            os.chdir("/")
            execute.osExecute(unmountlvm)
            os.rmdir(mountpoint)
        except:
            logging.info('Failed to unmount image/delete mount point')
            raise


