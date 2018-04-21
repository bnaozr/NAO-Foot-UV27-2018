#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 13:34:06 2018

@author: landaier
"""

import sys
import motion
import time
from naoqi import ALProxy
import math
import argparse

robotIp="localhost"
robotPort=11212

robotIp = "172.20.27.34"
robotPort = 9559

if (len(sys.argv) >= 2):
    robotIp = sys.argv[1]
if (len(sys.argv) >= 3):
    robotPort = int(sys.argv[2])

print (robotIp)
print (robotPort)

# Init proxies.
try:
    motionProxy = ALProxy("ALMotion", robotIp, robotPort)
except Exception, e:
    print( "Could not create proxy to ALMotion")
    print( "Error was: ", e)

try:
    postureProxy = ALProxy("ALRobotPosture", robotIp, robotPort)
except Exception, e:
    print( "Could not create proxy to ALRobotPosture")
    print( "Error was: ", e)
    
try:
    aup = ALProxy("ALAudioPlayer", robotIp, robotPort)
except Exception, e:
    print( "Could not create proxy to ALAudioPlayer")
    print( "Error was: ", e)

try:
    memoryProxy = ALProxy("ALMemory", robotIp, robotPort)
except Exception, e:
    print "Could not create proxy to ALMemory"
    print "Error was: ", e

try:
    sonarProxy = ALProxy("ALSonar", robotIp, robotPort)
except Exception, e:
    print "Could not create proxy to ALSonar"
    print "Error was: ", e


#IDLE_TO_READY = aup.loadFile("/tmp/grpel/vnao/py/Sound/IDLETOREADY.wav",0.5,1.0)
#ALL_TO_READY = aup.loadFile("tmp/grpel/vnao/py/Sound/ALLTOREADY.wav")
#READY_TO_AVANCE = aup.loadFile("tmp/grpel/vnao/py/Sound/READYTOAVANCE.wav")
#READY_TO_IDLE = aup.loadFile("tmp/grpel/vnao/py/Sound/READYTOIDLE.wav")
#READY_TO_RG = aup.loadFile("tmp/grpel/vnao/py/Sound/READYTORG.wav")
#READY_TO_RD = aup.loadFile("tmp/grpel/vnao/py/Sound/READYTORD.wav")

def cmdReady():
    motionProxy.move(0,0,0)    
    motionProxy.wakeUp()
    
def IDLEtoReady():
    try:   
        aup.post.playFile("/home/nao/music/IDLETOREADY.wav",0.7,0)
    except Exception : 
        return(None)
    return(None)

def AlltoReady():
    try:
        aup.post.playFile("/home/nao/music/ALLTOREADY.wav",0.7,0)
    except Exception : 
        return(None)
    return(None)

def ReadytoAvance():
    try :
        aup.post.playFile("/home/nao/music/READYTOAVANCE.wav",0.7,0)
    except Exception : 
        return(None)
    return(None)

def ReadytoIDLE():
    try:
        aup.post.playFile("/home/nao/music/READYTOIDLE.wav",0.7,0)
    except Exception : 
        return(None)
    return(None)
    
def ReadytoRG():
    try :
        aup.post.playFile("/home/nao/music/READYTORG.wav",0.7,0)
    except Exception : 
        return(None)
    return(None)


def ReadytoRD():
    try:
        aup.post.playFile("/home/nao/music/READYTORD.wav",0.7,0)
    except Exception : 
        return(None)
    return(None)


def AlltoBK():
    try:
        aup.post.playFile("/home/nao/music/ALLTOBACKWARD.wav",0.7,0)
    except Exception : 
        return(None)
    return(None)
    
def ReadytoShoot():
    try:
        aup.post.playFile("/home/nao/music/READYTOSHOOT.mp3",0.7,0)
    except Exception : 
        return(None)
    return(None)
    
    
def cmdIDLE():
    motionProxy.rest()

def cmdForward(x):
    motionProxy.move(x,0,0)

def cmdRG(tht):
    motionProxy.move(0,0,tht)

def cmdRD(tht):
    motionProxy.move(0,0,-tht)

def ObsG(d):
    sonarProxy.subscribe("SonarApp");
#    time.sleep(0.2)
    valL = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
    print valL
    sonarProxy.unsubscribe("SonarApp");
#    time.sleep(0.5-0.2)
    return(valL <= d)

def ObsD(d):
    sonarProxy.subscribe("SonarApp")
#   time.sleep(0.2)
    valR = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
    print(valR)
    sonarProxy.unsubscribe("SonarApp")
#    time.sleep(0.5-0.2)
    return(valR <= d)

