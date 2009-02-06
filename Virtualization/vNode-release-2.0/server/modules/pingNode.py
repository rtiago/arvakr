#!/usr/bin/python

import os,re,subprocess, sys
import time
from threading import Thread

class pingNodes(Thread):
    def __init__ (self,ip):
       Thread.__init__(self)
       self.ip = ip
       self.status = -1

    def run(self):
      ping_host = subprocess.Popen("ping -q -c2 -w2 -i0.2 "+self.ip,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
      lines = ping_host.stdout
      while 1:
        line = lines.readline()
        if not line: break
        igot = re.findall(pingNodes.lifeline,line)
        if igot:
           self.status = int(igot[0])

pingNodes.lifeline = re.compile(r"(\d) received")
report = ("No response","Partial Response","Alive")

def pingHosts(hostlist):
  pinglist = []
  pingAlive = []
  for host in hostlist:
    current = pingNodes(host)
    pinglist.append(current)
    current.start()

  for pingle in pinglist:
    pingle.join()
    if pingle.status == 2:
      pingAlive.append(pingle.ip)
  return pingAlive
