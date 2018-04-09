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

motionProxy.setWalkArmsEnabled(True, True)
motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

# Depuis naocmd -------------------------------------------------------

# functions (actions of the fsm)
# example of a function doRun 
def go():
    print ">>>>>> action : runs for his life"
    x = 1.0                             # depuis   naocmd
    y = 0.0                             # -
    theta = 0.0                         # -
    motionProxy.moveTo (x, y, theta)    # depuis naocmd
    time.sleep(1.0)
    event="PressG" # define the default event
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_w]:
        event="PressW"
    if key_pressed[pygame.K_s]:
        event="PressS" 
    return event # return event to be able to define the transition

def wakeUp():
    print ">>>>>> action : grabs a brush and puts a little make up"   # do some work
    motionProxy.wakeUp()                                                    # depuis naocmd
    motionProxy.setStiffnesses("Body", 1.0)                                 # --
    postureProxy.goToPosture("StandInit", 0.5)                              # --
    motionProxy.setWalkArmsEnabled(True, True)                              # --
    motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]]) # depuis naocmd
    time.sleep(1.0)
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
    print ">>>>>> action : stand still"   # do some work
    motionProxy.rest() # depuis naocmd
    time.sleep(1.0)
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

def turnLeft():
    print ">>>>>> action : turn left"   # do some work
    x = 0.2                             # depuis naocmd
    y = 0.0                             # --
    theta = math.pi/6.0                 # --
    motionProxy.moveTo (x, y, theta)    # depuis naocmd
    time.sleep(1.0)
    event="PressL" # define the default event
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_s]:
        event="PressS" 
    if key_pressed[pygame.K_w]:
        event="PressW" 
    return event

def turnRight():
    print ">>>>>> action : turn right"   # do some work
    x = 0.2                             # depuis naocmd
    y = 0.0                             # -
    theta = -math.pi/6.0                # -
    motionProxy.moveTo (x, y, theta)    # depuis naocmd
    time.sleep(1.0)
    event="PressR" # define the default event
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_s]:
        event="PressS"
    if key_pressed[pygame.K_w]:
        event="PressW"
    return event

def sleep():
    print ">>>>>> action : sleep"   # do some work
    postureProxy.goToPosture("Crouch", fractSpeed) # depuis naocmd
    motionProxy.setStiffnesses("Body", 0.0)        # -
    motionProxy.rest()                             # depuis naocmd
    time.sleep(1.0)
    event="PressS" # define the default event
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_s]:
        event="PressS"
    if key_pressed[pygame.K_w]:
        event="PressW"
    if key_pressed[pygame.K_e]:
        event="End"
    return event

def end():
    print ">>>>>> action : mission completed"   # do some work

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
   

    # defines the events 
    f.add_event("PressG") # example
    f.add_event("PressL")
    f.add_event("PressR")
    f.add_event("PressW")
    f.add_event("PressS")
    f.add_event("PressE")
   
   
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
    f.add_transition ("TournerGauche","Veille","PressS",sleep)
    f.add_transition ("TournerGauche","Pret","PressW",stand)
    f.add_transition ("TournerGauche","TournerGauche","PressL",turnLeft)
    f.add_transition ("Avancer","Pret","PressW",stand)
    f.add_transition ("Avancer","Veille","PressS",sleep)
    f.add_transition ("Avancer","Avancer","PressG",go)
    

    # initial state
    f.set_state ("Veille") # ... replace with your initial state
    # first event
    f.set_event ("PressW") # ...  replace with you first event 
    # end state
    end_state = "End" # ... replace  with your end state

 
    # fsm loop
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



