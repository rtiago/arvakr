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

import configNode, xendeployer, logging

class VNodeDeployer:
    def getDeployer(type):
        if (type == "xen"):
            return xendeployer.VNodeXenDeployer()
        raise Exception("Unknown deployer type '" + type + "'")
    getDeployer = staticmethod(getDeployer)

    def getDeployerForImage(imageTag):
        vnConfig = configNode.getVNodeNodeConfig()
        type = vnConfig.getVMType(imageTag)
        return VNodeDeployer.getDeployer(type)
    getDeployerForImage = staticmethod(getDeployerForImage)

    def createVirtualMachine(self, configFile, machinename, imagename, partitionSize, imageType):
        raise Exception('Abstract method, please override')

    def destroyVirtualMachine(self, machinename, imagename = None):
        raise Exception('Abstract method, please override')

    def checkAvailability(self, vmMemory, vmPartition, imageType):
        raise Exception('Abstract method, please override')
