#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 15:06:24 2018

@author: cuinatri
"""
from naoqi import ALProxy
from key import *
import sys
import time
from numpy.random import randint

# Init proxies.*
robotIP = "gammanao"
try:
    motionProxy = ALProxy("ALMotion", robotIP, 9559)
    sonarProxy = ALProxy("ALSonar", robotIP, 9559)
except Exception, e:
    print "Could not create proxy to ALMotion"
    print "Error was: ", e

try:
    postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
    sonarProxy.subscribe("myApplication")
except Exception, e:
    print "Could not create proxy to ALRobotPosture"
    print "Error was: ", e

# Set NAO in Stiffness On
pNames = "Body"
pStiffnessLists = 1.0
pTimeLists = 1.0
motionProxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

# Send NAO to Pose Init
postureProxy.goToPosture("StandInit", 0.5)

#####################
## Enable arms control by Walk algorithm
#####################
motionProxy.setWalkArmsEnabled(True, True)
#~ motionProxy.setWalkArmsEnabled(False, False)

memoryProxy = ALProxy("ALMemory", robotIP, 9559)

#####################
## FOOT CONTACT PROTECTION
#####################
#~ motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", False]])
motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

def doMotion():
    print ">>>>>> action : run for 1 s"   # do some work
    X = 0.8
    Y = 0.0
    Theta = 0.0
    Frequency = 1.0 # max speed
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
    global DD
    DD = ''
    time.sleep(0.2)
    newKey,val = getKey(); # check if key pressed
    event="Go" # define the default event
    if obstacle() : event = "Obstacle"
    elif newKey:
        if val==119:
            event="Wait"
        elif val==108:
            event="TurnL"
        elif val==114:
            event="TurnR"
        elif val==115:
            event="Stop"
    return event # return event to be able to define the transition
# define here all the other functions (actions) of the fsm 
# ...
    
def Turn(sens):
    X = 0.2
    global DD
    DD = ''
    if sens == 'R':
        Theta = -0.2
        Y = -0.5
    else:
        Theta = 0.2
        Y = 0.5
    Frequency = 1.0
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
    
def doWait():
    print ">>>>>> action : wait for 1 s"
    global DD
    DD = ''
    X = 0.0
    Y = 0.0
    Theta = 0.0
    Frequency = 0.0
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
    time.sleep(0.2)
    newKey,val = getKey(); # check if key pressed
    event="Wait" # define the default event
    if newKey:
        if val==103:
            event="Go"
        elif val==108:
            event="TurnL"
        elif val==114:
            event="TurnR"
        elif val==115:
            event="Stop"
    return event

def doTurnL():
    print ">>>>>> action : turn for 1 s"   # do some work
    Turn('L')
    time.sleep(0.2)
    newKey,val = getKey(); # check if key pressed
    event="TurnL" # define the default event
    if newKey:
        if val==119:
            event="Wait"
        elif val==103:
            event="Go"
        elif val==115:
            event="Stop"
        elif val==114:
            event="TurnR"
    return event

def doTurnR():
    print ">>>>>> action : turn for 1 s"   # do some work
    Turn('R')
    time.sleep(0.2)
    newKey,val = getKey() # check if key pressed
    event="TurnR" # define the default event
    if newKey:
        if val==119:
            event="Wait"
        elif val==103:
            event="Go"
        elif val==115:
            event="Stop"
        elif val==108:
            event="TurnL"
    return event

def doStopAll():
    print ">>>>>> action : stop all for 1 s"
    X = 0.0
    Y = 0.0
    Theta = 0.0
    Frequency = 0.0
    global DD
    DD = ''
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
    sys.exit(1)

DD=''

def doAvoid():
    X = 0.2
    global DD
    if DD not in [0,1] : k = randint(0,2)
    else : k = DD
    if k == 0 :
        Theta = -0.2
        Y = -0.5
    else:
        Theta = 0.2
        Y = 0.5
    DD = k
    Frequency = 1.0
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
    time.sleep(0.2)
    event = "Nothing"
    newKey,val = getKey()
    if newKey:
        if val==119:
            event="Wait"
        elif val==103:
            event="Go"
        elif val==115:
            event="Stop"
        elif val==108:
            event="TurnL"
        elif val==114:
            event="TurnR"
    elif obstacle() : event = "Obstacle"
    return event

def obstacle():
    # Get sonar left first echo (distance in meters to the first obstacle).
    le = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
    # Same thing for right.
    re = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
        # Get sonar left first echo (distance in meters to the first obstacle).
    time.sleep(0.1)
    le1 = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
    # Same thing for right.
    re1 = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
    print(re,re1,le,le1)
    seuil = 0.5
    if (re<seuil and re1<seuil) or (le<seuil and le1<seuil) or (le<seuil and re1<seuil) or (le1<seuil and re<seuil):
        return True
    else:
        return False