import fsm
import time
import pygame
import sys
import motion
from naoqi import ALProxy
import math
pygame.init()
pygame.display.set_mode((100, 100))

robotIp = "localhost"
robotPort = 11212

if (len(sys.argv) >= 2):
    robotIp = sys.argv[1]
if (len(sys.argv) >= 3):
    robotPort = int(sys.argv[2])

print(robotIp)
print(robotPort)


try:
    motionProxy = ALProxy("ALMotion", robotIp, robotPort)
except Exception:
    print("Could not create proxy to ALMotion")

try:
    postureProxy = ALProxy("ALRobotPosture", robotIp, robotPort)
except Exception:
    print("Could not create proxy to ALRobotPosture")

try:
    voicePxy = ALProxy("ALTextToSpeech", robotIp, robotPort)
except Exception:
    print("Could not create proxy to text2speech")
    
try:
    memoryProxy = ALProxy("ALMemory", robotIp, robotPort)
except Exception:
    print("Could not create proxy to text2speech")

try:
    sonarProxy = ALProxy("ALSonar", robotIp, robotPort)
except Exception:
    print("Could not create proxy to text2speech")

# Set NAO in Stiffness On 
# using wakeUp (new feature in 1.14.1)
motionProxy.wakeUp()
postureProxy.goToPosture("Crouch", 0.3)
motionProxy.setStiffnesses("Body", 0.0)



motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])


voicePxy.say("Bonjour")

# Definition des distances pour avancer ou tourner

x = 0.5
y = 0.0
theta1 = -math.pi/18
theta2 = math.pi/18
frequency = 1


# use keyboard to control the fsm
#  w : event "Wait"
#  s : event "Stop"
#  g : event "Go" 

# global variables
f = fsm.fsm();  # finite state machine

def getKey():
    cok=False
    c='s'
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            c=event.key
            cok=True
    print(pygame.K_w,c)
    return cok,c


def doRun():
    motionProxy.setWalkTargetVelocity(x, y, 0, frequency)
    print(">>>>>> action : run for 1 s")   # do some work
    sonarProxy.subscribe("myApplication")
    time.sleep(0.25)
    a = (memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value") < 1 )
    b = (memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value") < 1 )
    time.sleep(0.75)
    newKey,c = getKey(); # check if key pressed
    event = "Go"
    print(a,b)
    if newKey and not a and not b:
        if c==pygame.K_w:
            event="Wait"
        if c==pygame.K_r:
            event="TurnR"
        if c==pygame.K_l:
            event="TurnL"
        if c==pygame.K_g:
            event="Go"
        if c==pygame.K_s:
            event="Stop"
        if c==pygame.K_a:
            event="KickL"
        if c==pygame.K_p:
            event="KickR"
    elif a:
        while a:
            motionProxy.setWalkTargetVelocity(0, y, theta1, frequency)
            sonarProxy.subscribe("myApplication")
            time.sleep(0.25)
            a = (memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value") < 0.4 )
            time.sleep(0.75)
    else:
        while b:
            motionProxy.setWalkTargetVelocity(0, y, theta2, frequency)
            sonarProxy.subscribe("myApplication")
            time.sleep(0.25)
            b = (memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value") < 0.4 )
            time.sleep(0.75)
    return event

def TurnRight():
    motionProxy.setWalkTargetVelocity(0, y, theta1, frequency)
    print(">>>>>> action : rotation a droite pendant 1 s") 
    time.sleep(1.0)
    newKey,c = getKey(); # check if key pressed
    event = "TurnR"
    if newKey:
        if c==pygame.K_w:
            event="Wait"
        if c==pygame.K_l:
            event="TurnL"
        if c==pygame.K_g:
            event="Go"
        if c==pygame.K_s:
            event="Stop"
        if c==pygame.K_a:
            event="KickL"
        if c==pygame.K_p:
            event="KickR"
    return event

def TurnLeft():
    motionProxy.setWalkTargetVelocity(0, y, theta2, frequency)
    print(">>>>>> action : rotation a gauche pendant 1 s") 
    time.sleep(1.0)
    newKey,c = getKey(); # check if key pressed
    event = "TurnL"
    if newKey:
        if c==pygame.K_w:
            event="Wait"
        if c==pygame.K_r:
            event="TurnR"
        if c==pygame.K_g:
            event="Go"
        if c==pygame.K_s:
            event="Stop"
        if c==pygame.K_a:
            event="KickL"
        if c==pygame.K_p:
            event="KickR"
    return event

def doWait():
    motionProxy.stopMove()
    time.sleep(1.0)
    newKey,c = getKey(); # check if key pressed
    event = "Wait"
    if newKey:
        if c==pygame.K_r:
            event="TurnR"
        if c==pygame.K_l:
            event="TurnL"
        if c==pygame.K_g:
            event="Go"
        if c==pygame.K_s:
            event="Stop"
        if c==pygame.K_f:
            event="Fonctionne"
        if c==pygame.K_b:
            event="Bed"
        if c==pygame.K_a:
            event="KickL"
        if c==pygame.K_p:
            event="KickR"
    return event

def doCrouch():
    postureProxy.goToPosture("Crouch", 0.3)
    motionProxy.setStiffnesses("Body", 0.0)
    print(">>>>>> action : sleep d'1 s")
    time.sleep(1.0)
    newKey,c = getKey(); # check if key pressed
    event = "Bed"
    if newKey:
        if c==pygame.K_s:
            event="Stop"
        if c==pygame.K_f:
            event="Fonctionne"
    return event

def dofonctionne():
    postureProxy.goToPosture("StandInit", 0.5)
    motionProxy.setWalkArmsEnabled(True, True)
    print(">>>>>> action :Pret") 
    time.sleep(1.0)
    newKey,c = getKey(); # check if key pressed
    event = "Wait"
    if newKey:
        if c==pygame.K_r:
            event="TurnR"
        if c==pygame.K_g:
            event="Go"
        if c==pygame.K_s:
            event="Stop"
        if c==pygame.K_b:
            event="Bed"
        if c==pygame.K_l:
            event="TurnL"
        if c==pygame.K_a:
            event="KickL"
        if c==pygame.K_p:
            event="KickR"
    return event

def Stop():
    motionProxy.stopMove()
    postureProxy.goToPosture("Crouch", 0.3)
    motionProxy.setStiffnesses("Body", 0.0)
    print(">>>>>> Fin du programme") 
    return "Stop"

''' Elements utilises dans les fonctions de tir '''


axisMask     = 63
space        = motion.FRAME_ROBOT
dx      = 0.05                 
dz      = 0.05                 
dwy     = 5.0*math.pi/180.0
times   = [2.0, 2.7, 4.5]
isAbsolute = False
targetList = [
[-dx, 0.0, dz, 0.0, +dwy, 0.0],
[+dx, 0.0, dz, 0.0, 0.0, 0.0],
[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

def KickOn():
    motionProxy.stopMove()
    motionProxy.stiffnessInterpolation("Body",1.0,1.0)
    postureProxy.goToPosture("StandInit",0.5)
    motionProxy.wbEnable(True)
    motionProxy.wbFootState("Fixed","Legs")
    motionProxy.wbEnableBalanceConstraint(True, "Legs")
    return None

def KickOff():
    motionProxy.wbEnable(False)
    motionProxy.stiffnessInterpolation("Body",1.0,1.0)
    postureProxy.goToPosture("StandInit",0.5)
    return None
    

def KickRight():
    KickOn()
    Shooting_Leg= "RLeg"
    SupportLeg= "LLeg"
    motionProxy.wbGoToBalance(SupportLeg, 2.0)
    motionProxy.wbFootState("Free", Shooting_Leg)
    motionProxy.positionInterpolation(Shooting_Leg, space, targetList,axisMask, times, isAbsolute)
    KickOff()
    print(">>>>>> action : Tir Droit")
    time.sleep(1.0)
    newKey,c = getKey();
    event = "Wait"
    if newKey:
        if c==pygame.K_s:
            event="Stop"
        if c==pygame.K_w:
            event="Wait"
    return event

def KickLeft():
    KickOn()
    Shooting_Leg= "LLeg"
    SupportLeg= "RLeg"
    motionProxy.wbGoToBalance(SupportLeg, 2.0)
    motionProxy.wbFootState("Free", Shooting_Leg)
    motionProxy.positionInterpolation(Shooting_Leg, space, targetList,axisMask, times, isAbsolute)
    KickOff()
    print(">>>>>> action : Tir Gauche")
    time.sleep(1.0)
    newKey,c = getKey();
    event = "Wait"
    if newKey:
        if c==pygame.K_s:
            event="Stop"
        if c==pygame.K_w:
            event="Wait"
    return event
    

if __name__== "__main__":
    
    # define the states
    f.add_state ("Idle")
    f.add_state ("Ready")
    f.add_state ("Deplacement")
    f.add_state ("Rotation")
    f.add_state ("End")
    f.add_state ("Kick")

    # defines the events 
    f.add_event ("Wait")
    f.add_event ("Go")
    f.add_event ("TurnR")
    f.add_event ("TurnL")
    f.add_event ("Stop")
    f.add_event ("Fonctionne")
    f.add_event ("Bed")
    f.add_event ("KickR")
    f.add_event ("KickL")
   
    # defines the transition matrix
    # current state, next state, event, action in next state
    f.add_transition ("Ready","Ready","Wait",doWait); # example
    f.add_transition ("Ready","Deplacement","Go",doRun);
    f.add_transition ("Ready","Rotation","TurnR",TurnRight);
    f.add_transition ("Ready","Rotation","TurnL",TurnLeft);
    f.add_transition ("Ready","End","Stop",Stop);
    f.add_transition ("Ready","Idle","Bed",doCrouch);
    f.add_transition ("Ready","Kick","KickR",KickRight);
    f.add_transition ("Ready","Kick","KickL",KickLeft);
    
    f.add_transition ("Rotation","Ready","Wait",doWait);
    f.add_transition ("Rotation","Rotation","TurnR",TurnRight);
    f.add_transition ("Rotation","Rotation","TurnL",TurnLeft);
    f.add_transition ("Rotation","End","Stop",Stop);
    f.add_transition ("Rotation","Deplacement","Go",doRun);
    f.add_transition ("Rotation","Kick","KickR",KickRight);
    f.add_transition ("Rotation","Kick","KickL",KickLeft);
    
    f.add_transition ("Deplacement","Deplacement","Go",doRun);
    f.add_transition ("Deplacement","Ready","Wait",doWait);
    f.add_transition ("Deplacement","Rotation","TurnL",TurnLeft);
    f.add_transition ("Deplacement","Rotation","TurnR",TurnRight);
    f.add_transition ("Deplacement","End","Stop",Stop);
    f.add_transition ("Deplacement","Kick","KickR",KickRight);
    f.add_transition ("Deplacement","Kick","KickL",KickLeft);
    
    f.add_transition ("Idle","Ready","Fonctionne",dofonctionne);
    f.add_transition ("Idle","End","Stop",Stop);
    f.add_transition ("Idle","Idle","Bed",doCrouch);
    
    f.add_transition ("Kick","Ready","Wait",doWait);
    f.add_transition ("Kick","End","Stop",Stop);
    
    # initial state
    f.set_state ("Idle") # ... replace with your initial state
    # first event
    f.set_event ("Bed") # ...  replace with you first event 
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



