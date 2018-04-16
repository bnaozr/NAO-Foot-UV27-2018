import fsm
import time
import sys
import pygame
import motion
from naoqi import ALProxy
import math

pygame.init()
pygame.display.set_mode((100,  100))
# use keyboard to control the fsm
#  w : event "Wait"
#  s : event "Stop"
#  g : event "Go" 

# global variables
f = fsm.fsm();  # finite state machine

##Depuis nao cmd ------------------------------------------------------
#Robot ports
robotIp="172.20.26.29"
robotIp="betanao"
robotIp="172.20.11.241"
robotPort=9559

robotIp="localhost"
robotPort=11212

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
    voicePxy = ALProxy("ALTextToSpeech", robotIp, robotPort)
except Exception, e:
    print "Could not create proxy to text2speech"
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

motionProxy.setWalkArmsEnabled(True, True)
motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

# Depuis naocmd -------------------------------------------------------

# functions (actions of the fsm)
# example of a function doRun 
def go():
    global transitionState
    print ">>>>>> action : runs for his life"
    sonarProxy.subscribe("SonarApp")
    valL = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
    valR = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
    sonarProxy.unsubscribe("SonarApp")
    if (valL<=0.3 or valR<=0.3):
        motionProxy.stopMove()
        event="Obstacle"
    else:
        x  = 1.0
        y  = 0.0
        theta  = 0.0
        frequency  = 0.75
        motionProxy.setWalkTargetVelocity(x, y, theta, frequency)
        event="PressG" # define the default event
        key_pressed = pygame.key.get_pressed()

        transitionState = None
        if key_pressed[pygame.K_w]:
            motionProxy.stopMove()
            event="PressW"
        if key_pressed[pygame.K_s]:
            motionProxy.stopMove()
            event="PressS" 
        if key_pressed[pygame.K_r]:
            motionProxy.stopMove()
            event = "PressW"
            transitionState = "PressR"
        if key_pressed[pygame.K_l]:
            motionProxy.stopMove()
            event = "PressW"
            transitionState = "PressL"
        if key_pressed[pygame.K_e]:
            motionProxy.stopMove()
            event = "PressS"
            transitionState = "PressE"
            
    return event # return event to be able to define the transition

def wakeUp():
    print ">>>>>> action : grabs a brush and puts a little make up"   # do some work
    motionProxy.wakeUp()                                                    # depuis naocmd
    motionProxy.setStiffnesses("Body", 1.0)                                 # --
    postureProxy.goToPosture("StandInit", 0.5)                              # --
    motionProxy.setWalkArmsEnabled(True, True)                              # --
    motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]]) # depuis naocmd
    event="PressW" # define the default event
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_g]:
        event="PressG"  
    if key_pressed[pygame.K_s]:
        event="PressS" 
    if key_pressed[pygame.K_l]:
        event="PressL" 
    if key_pressed[pygame.K_r]:
        event="PressR" 
        
    return event

def stand():
    print ">>>>>> action : stand still"   # depuis naocmd
    global transitionState
    event="PressW" # define the default event
    
    if transitionState == None:
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_g]:
            time.sleep(1.0)
            event="PressG"  
        if key_pressed[pygame.K_s]:
            time.sleep(1.0)
            event="PressS" 
        if key_pressed[pygame.K_l]:
            time.sleep(1.0)
            event="PressL" 
        if key_pressed[pygame.K_r]:
            time.sleep(1.0)
            event="PressR"
    elif transitionState == "PressG":
        event = "PressG"
    elif transitionState == "PressL":
        event = "PressL"
    elif transitionState == "PressR":
        event = "PressR"
    elif transitionState == "PressE":
        event = "PressE"
    return event

def turnLeft():
    print ">>>>>> action : turn left"   # do some work
    global transitionState
    x  = 0.1
    y  = 0.0
    theta  = math.pi/4.0 
    frequency  = 0.75
    motionProxy.setWalkTargetVelocity(x, y, theta, frequency)
    event="PressL" # define the default event
    key_pressed = pygame.key.get_pressed()
    transitionState = None
    if key_pressed[pygame.K_s]:
        motionProxy.stopMove()
        event="PressS"
    if key_pressed[pygame.K_w]:
        motionProxy.stopMove()
        event="PressW"
    if key_pressed[pygame.K_r]:
        motionProxy.stopMove()
        event = "PressW"
        transitionState = "PressR"
    if key_pressed[pygame.K_g]:
        motionProxy.stopMove()
        event = "PressW"
        transitionState = "PressG"
    if key_pressed[pygame.K_e]:
        motionProxy.stopMove()
        event = "PressS"
        transitionState = "PressE"

    return event

def turnRight():
    print ">>>>>> action : turn right"   # do some work
    global transitionState
    x  = 0.1
    y  = 0.0
    theta  = -math.pi/4.0 
    frequency  = 0.75
    motionProxy.setWalkTargetVelocity(x, y, theta, frequency)
    event="PressR" # define the default event
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_s]:
        motionProxy.stopMove()
        event="PressS"
    if key_pressed[pygame.K_w]:
        motionProxy.stopMove()
        event="PressW"
    if key_pressed[pygame.K_l]:
        motionProxy.stopMove()
        event = "PressW"
        transitionState = "PressL"
    if key_pressed[pygame.K_g]:
        motionProxy.stopMove()
        event = "PressW"
        transitionState = "PressG"
    if key_pressed[pygame.K_e]:
        motionProxy.stopMove()
        event = "PressS"
        transitionState = "PressE"
        
    return event

def sleep():
    print ">>>>>> action : sleep"   # do some work
    global transitionState
    motionProxy.rest()                             # depuis naocmd
    event="PressS" # define the default event
    key_pressed = pygame.key.get_pressed()
    if transitionState == None:
        if key_pressed[pygame.K_s]:
            event="PressS"
        if key_pressed[pygame.K_w]:
            event="PressW"
        if key_pressed[pygame.K_e]:
            event="End"
    elif transitionState == "PressE":
        event = "End"

        
    return event

def end():
    print ">>>>>> action : mission completed"   # do some work


def evitement():
    print ">>>>>> action : attention a la mousse"   # do some work
    sonarProxy.subscribe("SonarApp")
    valL = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
    valR = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
    sonarProxy.unsubscribe("SonarApp")
    x  = 0.1
    y  = 0.0
    frequency=0.75
    while valR<valL or valL<valR:
        if valR<valL:
            theta  = math.pi/4.0 
            motionProxy.setWalkTargetVelocity(x, y, theta, frequency)
            sonarProxy.subscribe("SonarApp")
            valR = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
            valL = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
            sonarProxy.unsubscribe("SonarApp")
        elif valL <valR:
            theta  =-math.pi/4.0 
            motionProxy.setWalkTargetVelocity(x, y, theta, frequency)
            sonarProxy.subscribe("SonarApp")
            valL = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
            sonarProxy.unsubscribe("SonarApp")
    motionProxy.stopMove()
    event="FinObstacle"

    return event

# define here all the other functions (actions) of the fsm 
# ...

if __name__== "__main__":
    
    # define the states
    f.add_state ("Pret") # example
    f.add_state ("Avancer")
    f.add_state ("Veille")
    f.add_state ("TournerDroite")
    f.add_state ("TournerGauche")
    f.add_state ("End")
    f.add_state ("Evitement")

    # defines the events 
    f.add_event("PressG") # example
    f.add_event("PressL")
    f.add_event("PressR")
    f.add_event("PressW")
    f.add_event("PressS")
    f.add_event("PressE")
    f.add_event("Obstacle")
   
   
    # defines the transition matrix
    # current state, next state, event, action in next state
    f.add_transition ("Veille","Veille","PressS",sleep)
    f.add_transition ("Veille","Pret","PressW",wakeUp)
    f.add_transition ("Veille","End","PressE",end)
    f.add_transition ("Pret","Veille","PressS",sleep)
    f.add_transition ("Pret","TournerDroite","PressR",turnRight)
    f.add_transition ("Pret","TournerGauche","PressL",turnLeft)
    f.add_transition ("Pret","Avancer","PressG",go)
    f.add_transition ("Pret","Pret","PressW",stand)
    f.add_transition ("TournerDroite","Pret","PressW",stand)
    f.add_transition ("TournerDroite","Veille","PressS",sleep)
    f.add_transition ("TournerDroite","TournerDroite","PressR",turnRight)
    f.add_transition ("TournerDroite","TournerGauche","PressL",turnLeft)
    f.add_transition ("TournerDroite","Avancer","PressG",go)
    f.add_transition ("TournerGauche","Veille","PressS",sleep)
    f.add_transition ("TournerGauche","Pret","PressW",stand)
    f.add_transition ("TournerGauche","TournerGauche","PressL",turnLeft)
    f.add_transition ("TournerGauche","TournerDroite","PressR",turnRight)
    f.add_transition ("TournerGauche","Avancer","PressG",go)
    f.add_transition ("Avancer","Pret","PressW",stand)
    f.add_transition ("Avancer","Veille","PressS",sleep)
    f.add_transition ("Avancer","Avancer","PressG",go)
    f.add_transition ("Avancer","Evitement","Obstacle",evitement)
    f.add_transition ("Avancer","TournerGauche","PressL",turnLeft)
    f.add_transition ("Avancer","TournerDroite","PressR",turnRight)
    f.add_transition ("Evitement","Avancer","FinObstacle",go)
    

    # initial state
    f.set_state ("Veille") # ... replace with your initial state
    # first event
    f.set_event ("PressW") # ...  replace with you first event 
    # end state
    end_state = "End" # ... replace  with your end state

 
    # fsm loop
    transitionState = None
    run = True   
    while (run):
        pygame.event.pump()
        funct = f.run () # function to be executed in the new state
        if f.curState != end_state:
            newEvent = funct() # new event when state action is finished
            print "New Event : ",newEvent
            f.set_event(newEvent) # set new event for next transition
        else:
            funct()
            run = False
            
print "End of the programm"