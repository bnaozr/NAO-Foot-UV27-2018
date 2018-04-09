# -*- coding: utf-8 -*-
import fsm
import time
import sys
import select 
import pygame
import motion
from naoqi import ALProxy
import math

pygame.init()
# draw a little area (to fucus on to get keys)
pygame.display.set_mode((100,  100))

# global variables
f = fsm.fsm();  # finite state machine
tseq= 0.5
fractSpeed=0.8
global is_sleeping
is_sleeping = False
global evitement
evitement = False

robotIp="localhost"
robotPort=11216

if (len(sys.argv) >= 2):
    robotIp = sys.argv[1]
if (len(sys.argv) >= 3):
    robotPort = int(sys.argv[2])

print robotIp
print robotPort

# Init proxies.
try:
    motionProxy = ALProxy("ALMotion", robotIp, robotPort)
except Exception, e:
    print "Could not create proxy to ALMotion"
    print "Error was: ", e

try:
    postureProxy = ALProxy("ALRobotPosture", robotIp, robotPort)
except Exception, e:
    print "Could not create proxy to ALRobotPosture"
    print "Error was: ", e
    
try:
    tts = ALProxy("ALTextToSpeech", robotIp, robotPort)
except Exception, e:
    print "Could not create proxy to speak"
    print "Error was: ", e
    
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


#Now you can retrieve sonar data from ALMemory.


motionProxy.wakeUp()
motionProxy.setStiffnesses("Body", 1.0)



def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def getKey():
    c='s'
    cok=False
    if isData():
        c = sys.stdin.read(1)
        cok=True
    return cok,c

# use keyboard to control the fsm
#  s : event "Stop"
#  g : event "Go" 
#  s : terminer la mission
#  l : tourner à gauche
#  r : tourner à droite


# functions (actions of the fsm)
def possibilityIdle():
    global is_sleeping
    if is_sleeping == False:
        postureProxy.goToPosture("Crouch", fractSpeed)
        time.sleep(tseq/2)
        motionProxy.setStiffnesses("Body", 0.0)
        tts.say("Tuer tous les humains ! Tuer tous les humain !")
    event="Stay" # define the default event
    is_sleeping = True
    time.sleep(tseq/2)
    for even in pygame.event.get():
        if even.type == pygame.QUIT:
            sys.exit()
        if even.type == pygame.KEYDOWN:
            if even.key == pygame.K_s:
                event="Start"
    return event

def possibilityStart():
    global is_sleeping
#    sonarProxy.subscribe("SonarApp");
#    time.sleep(0.25)
#    valL = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
#    valR = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
#    sonarProxy.unsubscribe("SonarApp");
    is_sleeping = False
    motionProxy.setStiffnesses("Body", 1.0)
    X = 0.0
    Y = 0.0
    Theta = 0.0
    Frequency = 0.8
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency) # do some work # do some work
    postureProxy.goToPosture("StandInit", fractSpeed)
    time.sleep(tseq)
    event="Stay" # define the default event
    for even in pygame.event.get():
        if even.type == pygame.QUIT:
            sys.exit()
        if even.type == pygame.KEYDOWN:
            if even.key == pygame.K_UP:
                event="MoveForward"
            elif even.key == pygame.K_DOWN:
                event="MoveBackward" 
            elif even.key == pygame.K_LEFT:
                event="RotateLeft"
            elif even.key == pygame.K_RIGHT:
                event="RotateRight" 
            elif even.key == pygame.K_p:
                event="Pause" 
            elif even.key == pygame.K_k:
                event="Kill"    
            elif even.key == pygame.K_SPACE:
                event="Shoot"   
    return event

def possibilityStop():
    global is_sleeping
    print(">>>>>> Robot Killed")  # do some work
    if is_sleeping == False:
        postureProxy.goToPosture("Crouch", fractSpeed)
        time.sleep(tseq/2)
        motionProxy.setStiffnesses("Body", 0.0)
        time.sleep(tseq/2)
        time.sleep(1.0)
    event="Stay" # define the default event
    is_sleeping = True
    time.sleep(1.0)
    for even in pygame.event.get():
        if even.type == pygame.QUIT:
            sys.exit()
    return event

def possibilityForward():
#    global evitement
    X = 0.5
    Y = 0.0
#    if evitement:
#        Theta = 0.5
#    else:
    Theta = 0.0
    Frequency = 0.8
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency) # do some work
    time.sleep(tseq)
    event="Stay" # define the default event
#    sonarProxy.subscribe("SonarApp");
#    time.sleep(0.25)
#    valL = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
#    valR = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
#    sonarProxy.unsubscribe("SonarApp");
#    if max(valR, valL) <= 0.5 :
#        print("J'AI DETECTE UN OBJET")
#        evitement = True
#    else:
#        evitement = False
    for even in pygame.event.get():
        if even.type == pygame.QUIT:
            sys.exit()
        if even.type == pygame.KEYDOWN:
            if even.key == pygame.K_s:
                event="StopMove"
            elif even.key == pygame.K_DOWN:
                event="StopMove"
            elif even.key == pygame.K_LEFT:
                event="RotateLeft"
            elif even.key == pygame.K_RIGHT:
                event="RotateRight" 
    return event # return event to be able to define the transition

def possibilityBackward():
    X = -0.5
    Y = 0.0
    Theta = 0.0
    Frequency = 0.8
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency) # do some work
    time.sleep(tseq)
    event="Stay" # define the default event
    for even in pygame.event.get():
        if even.type == pygame.QUIT:
            sys.exit()
        if even.type == pygame.KEYDOWN:
            if even.key == pygame.K_s:
                event="StopMove"
#                X = 0.0
#                Y = 0.0
#                Theta = 0.0
#                Frequency = 0.8
#                motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
            elif even.key == pygame.K_LEFT:
                event="RotateLeft"
            elif even.key == pygame.K_RIGHT:
                event="RotateRight"
            elif even.key == pygame.K_UP:
                event="StopMove"
    return event # return event to be able to define the transition

def possibilityRight():
    X = 0.0
    Y = 0.0
    Theta = -0.5
    Frequency = 0.8
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)  # do some work
    time.sleep(tseq)
    event="Stay" # define the default event
    for even in pygame.event.get():
        if even.type == pygame.QUIT:
            sys.exit()
        if even.type == pygame.KEYDOWN:
            if even.key == pygame.K_s:
                event="StopRotate"
#                X = 0.0
#                Y = 0.0
#                Theta = 0.0
#                Frequency = 0.8
#                motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
            elif even.key == pygame.K_UP:
                event="MoveForward"
            elif even.key == pygame.K_DOWN:
                event="MoveBackward"  
            elif even.key == pygame.K_LEFT:
                event="StopRotate"
    return event

def possibilityLeft():
    X = 0.0
    Y = 0.0
    Theta = 0.5
    Frequency = 0.8
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency) # do some work
    time.sleep(tseq)
    event="Stay" # define the default event
    for even in pygame.event.get():
        if even.type == pygame.QUIT:
            sys.exit()
        if even.type == pygame.KEYDOWN:
            if even.key == pygame.K_s:
                event="StopRotate"
#                X = 0.0
#                Y = 0.0
#                Theta = 0.0
#                Frequency = 0.8
#                motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
            elif even.key == pygame.K_UP:
                event="MoveForward"
            elif even.key == pygame.K_DOWN:
                event="MoveBackward"    
            elif even.key == pygame.K_RIGHT:
                event="StopRotate"
    return event

def possibilityBackwardLeft():
    X = -1
    Y = 0.0
    Theta = 0.5
    Frequency = 0.8
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency) # do some work
    time.sleep(tseq)
    event="Stay" # define the default event
    for even in pygame.event.get():
        if even.type == pygame.QUIT:
            sys.exit()
        if even.type == pygame.KEYDOWN:
            if even.key == pygame.K_s:
                event="Stop"
#                X = 0.0
#                Y = 0.0
#                Theta = 0.0
#                Frequency = 0.8
#                motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
            elif even.key == pygame.K_DOWN:
                event="MoveBackward" 
            elif even.key == pygame.K_LEFT:
                event="RotateLeft"  
            
            elif even.key == pygame.K_UP:
                event="StopMove"
            elif even.key == pygame.K_RIGHT:
                event="StopRotate" 
    return event # return event to be able to define the transition

def possibilityBackwardRight():
    X = -0.5
    Y = 0.0
    Theta = -0.5
    Frequency = 0.8
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency) # do some work
    time.sleep(tseq)
    event="Stay" # define the default event
    for even in pygame.event.get():
        if even.type == pygame.QUIT:
            sys.exit()
        if even.type == pygame.KEYDOWN:
            if even.key == pygame.K_s:
                event="Stop"
#                X = 0.0
#                Y = 0.0
#                Theta = 0.0
#                Frequency = 0.8
#                motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
            elif even.key == pygame.K_DOWN:
                event="MoveBackward" 
            elif even.key == pygame.K_RIGHT:
                event="RotateRight"  
                
            elif even.key == pygame.K_LEFT:
                event="StopRotate"
            elif even.key == pygame.K_UP:
                event="StopMove"
    return event # return event to be able to define the transition

def possibilityForwardLeft():
    X = 0.5
    Y = 0.0
    Theta = 0.5
    Frequency = 0.8
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency) # do some work
    time.sleep(tseq)
    event="Stay" # define the default event
    for even in pygame.event.get():
        if even.type == pygame.QUIT:
            sys.exit()
        if even.type == pygame.KEYDOWN:
            if even.key == pygame.K_s:
                event="Stop"
#                X = 0.0
#                Y = 0.0
#                Theta = 0.0
#                Frequency = 0.8
#                motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
            elif even.key == pygame.K_UP:
                event="MoveForward"
            elif even.key == pygame.K_LEFT:
                event="RotateLeft"
                
            elif even.key == pygame.K_DOWN:
                event="StopMove" 
            elif even.key == pygame.K_RIGHT:
                event="StopRotate" 
    return event # return event to be able to define the transition

def possibilityForwardRight():
    X = 0.5
    Y = 0.0
    Theta = -0.5
    Frequency = 0.8
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency) # do some work
    time.sleep(tseq)
    event="Stay" # define the default event
    for even in pygame.event.get():
        if even.type == pygame.QUIT:
            sys.exit()
        if even.type == pygame.KEYDOWN:
            if even.key == pygame.K_s:
                event="Stop"
#                X = 0.0
#                Y = 0.0
#                Theta = 0.0
#                Frequency = 0.8
#                motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
            elif even.key == pygame.K_UP:
                event="MoveForward"
            elif even.key == pygame.K_RIGHT:
                event="RotateRight" 
                
            elif even.key == pygame.K_DOWN:
                event="StopMove" 
            elif even.key == pygame.K_LEFT:
                event="StopRotate" 
    return event # return event to be able to define the transition


def doShoot():
  isEnabled  = True
  motionProxy.wbEnable(isEnabled)
  # Activate Whole Body Balancer
  isEnabled  = True
  motionProxy.wbEnable(isEnabled)
  # Legs are constrained fixed
  stateName  = "Fixed"
  supportLeg = "Legs"
  motionProxy.wbFootState(stateName, supportLeg)
  # Constraint Balance Motion
  isEnable   = True
  supportLeg = "Legs"
  motionProxy.wbEnableBalanceConstraint(isEnable, supportLeg)
  # Com go to LLeg
  supportLeg = "LLeg"
  duration   = 1.0
  motionProxy.wbGoToBalance(supportLeg, duration)
  # RLeg is free
  stateName  = "Free"
  supportLeg = "RLeg"
  motionProxy.wbFootState(stateName, supportLeg)
  # RLeg is optimized
  effectorName = "RLeg"
  axisMask     = 63
  space        = motion.FRAME_ROBOT
  # Motion of the RLeg
  dx      = 0.13                # translation axis X (meters)
  dz      = 0.05             # translation axis Z (meters)
  dwy     = 2.0*math.pi/180.0    # rotation axis Y (radian)
  times   = [1.5, 1.9, 3]
  isAbsolute = False
  targetList = [
    [-0.05, 0.0, dz, 0.0, +dwy, 0.0],
    [+dx, 0.0, dz, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
  motionProxy.positionInterpolation(effectorName, space, targetList, axisMask, times, isAbsolute)
  # Deactivate Head tracking
  isEnabled    = False
  motionProxy.wbEnable(isEnabled)
  # send robot to Pose Init
  postureProxy.goToPosture("StandInit", 0.5)
  event="Stay"
  return event
    

if __name__== "__main__":
    # define the states
    f.add_state ("Idle") 
    f.add_state ("Start") 
    f.add_state ("Left") 
    f.add_state ("Right")
    f.add_state ("Stop") 
    f.add_state ("Forward")
    f.add_state ("Backward") 
    f.add_state ("ForwardRight")
    f.add_state ("ForwardLeft")
    f.add_state ("BackwardRight") 
    f.add_state ("BackwardLeft") 
    f.add_state ("Shoot")

    # defines the events 
    f.add_event ("Launch")
    f.add_event ("MoveForward")
    f.add_event ("MoveBackward")
    f.add_event ("RotateLeft")
    f.add_event ("RotateRight")
    f.add_event ("Kill")
    f.add_event ("StopMove")
    f.add_event ("StopRotate")
    f.add_event ("Pause")
    f.add_event ("Stay")
    f.add_event ("Stop")
    f.add_event ("Shoot")
    
   
    # defines the transition matrix
    # current state, next state, event, action in next state
    f.add_transition ("Idle","Idle","Stay",possibilityIdle);
    f.add_transition ("Start","Start","Stay",possibilityStart);
    f.add_transition ("Stop","Stop","Stay",possibilityStop);
    
    f.add_transition ("Idle","Start","Start",possibilityStart);
    f.add_transition ("Start","Forward","MoveForward",possibilityForward);
    f.add_transition ("Start","Backward","MoveBackward",possibilityBackward);
    f.add_transition ("Forward","Forward","Stay",possibilityForward);
    f.add_transition ("Backward","Backward","Stay",possibilityBackward);
    f.add_transition ("Forward","Start","StopMove",possibilityStart);
    f.add_transition ("Backward","Start","StopMove",possibilityStart);
    
    f.add_transition ("Start","Left","RotateLeft",possibilityLeft);
    f.add_transition ("Start","Right","RotateRight",possibilityRight);
    f.add_transition ("Left","Left","Stay",possibilityLeft);
    f.add_transition ("Right","Right","Stay",possibilityRight);
    f.add_transition ("Left","Start","StopRotate",possibilityStart);
    f.add_transition ("Right","Start","StopRotate",possibilityStart);
    
    f.add_transition ("Start","Idle","Pause",possibilityIdle);
    f.add_transition ("Start","Stop","Kill",possibilityStop);
    
    f.add_transition ("ForwardLeft","ForwardLeft","Stay",possibilityForwardLeft);
    f.add_transition ("ForwardRight","ForwardRight","Stay",possibilityForwardRight);
    f.add_transition ("BackwardLeft","BackwardLeft","Stay",possibilityBackwardLeft);
    f.add_transition ("BackwardRight","BackwardRight","Stay",possibilityBackwardRight);
    
    f.add_transition ("Forward","ForwardLeft","RotateLeft",possibilityForwardLeft);
    f.add_transition ("Forward","ForwardRight","RotateRight",possibilityForwardRight);
    f.add_transition ("Backward","BackwardLeft","RotateLeft",possibilityBackwardLeft);
    f.add_transition ("Backward","BackwardRight","RotateRight",possibilityBackwardRight);
    
    f.add_transition ("Left","ForwardLeft","MoveForward",possibilityForwardLeft);
    f.add_transition ("Right","ForwardRight","MoveForward",possibilityForwardRight);
    f.add_transition ("Left","BackwardLeft","MoveBackward",possibilityBackwardLeft);
    f.add_transition ("Right","BackwardRight","MoveBackward",possibilityBackwardRight);
    
    f.add_transition ("ForwardLeft","Forward","StopRotate",possibilityForward);
    f.add_transition ("ForwardRight","Forward","StopRotate",possibilityForward);
    f.add_transition ("BackwardLeft","Backward","StopRotate",possibilityBackward);
    f.add_transition ("BackwardRight","Backward","StopRotate",possibilityBackward);
    
    f.add_transition ("ForwardLeft","Left","StopMove",possibilityLeft);
    f.add_transition ("ForwardRight","Right","StopMove",possibilityRight);
    f.add_transition ("BackwardLeft","Left","StopMove",possibilityLeft);
    f.add_transition ("BackwardRight","Right","StopMove",possibilityRight);
    
    f.add_transition ("ForwardLeft","Start","Stop",possibilityStart);
    f.add_transition ("ForwardRight","Start","Stop",possibilityStart);
    f.add_transition ("BackwardLeft","Start","Stop",possibilityStart);
    f.add_transition ("BackwardRight","Start","Stop",possibilityStart);
    
    f.add_transition ("Start","Shoot","Shoot",doShoot);
    f.add_transition ("Shoot","Start","Stay",possibilityStart);
    
    is_sleeping = False
    
    # initial state
    f.set_state ("Idle") # ... replace with your initial state
    # first event
    f.set_event ("Stay") # ...  replace with you first event 
    # end state
    end_state = "End" # ... replace  with your end state

    # fsm loop
    run = True   
    while (run):
        funct = f.run () # function to be executed in the new state
        if f.curState != end_state:
            newEvent = funct() # new event when state action is finished
            print("New Event : ",newEvent)
            f.set_event(newEvent) # set new event for next transition
        else:
            funct()
            run = False
            
    print("End of the programm")



