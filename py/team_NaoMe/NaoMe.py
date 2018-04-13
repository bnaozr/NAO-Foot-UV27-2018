import fsm
import time
import pygame
import sys
import motion
from naoqi import ALProxy
import math
import argparse
import almath
from numpy.random import randint
pygame.init()
pygame.display.set_mode((100, 100))

DD = randint(0,2)
robotIp = "localhost"
robotPort = 11212
State = ""

if (len(sys.argv) >= 2):
    robotIp = sys.argv[1]
if (len(sys.argv) >= 3):
    robotPort = int(sys.argv[2])

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

# Partie pour Déterminer la Position du Robot
try:
    import pylab as pyl
    PLOT_ALLOW = True
except ImportError:
    print "Matplotlib not found. this example will not plot data"
    PLOT_ALLOW = False
 
# get robotPosition and nextRobotPosition
    useSensors = False
    robotPosition     = almath.Pose2D(motionProxy.getRobotPosition(useSensors))
    nextRobotPosition = almath.Pose2D(motionProxy.getNextRobotPosition())
 
# here we wait until the move process is over
    motionProxy.waitUntilMoveIsFinished()
    # then we get the final robot position
    robotPositionFinal = almath.Pose2D(motionProxy.getRobotPosition(False))

    # compute robot Move with the second call of move API
    # so between nextRobotPosition and robotPositionFinal
    robotMove = almath.pose2DInverse(nextRobotPosition)*robotPositionFinal
    print ("Robot Move:", robotMove)

    # Go to rest position
    motionProxy.rest()

    # end compute, begin plot

    if PLOT_ALLOW:
        #################
        # Plot the data #
        #################
        pyl.figure()
        printRobotPosition(robotPosition, 'black')
        printRobotPosition(nextRobotPosition, 'blue')
        printFootSteps(footSteps1, 'green', 'red')

        pyl.figure()
        printRobotPosition(robotPosition, 'black')
        printRobotPosition(nextRobotPosition, 'blue')
        printFootSteps(footSteps2, 'blue', 'orange')

        pyl.show()

        # end plot

def printRobotPosition(pos, color):
    """ Function for plotting a robot position
        :param pos: an almath Pose2D
        :param color: the color of the robot
    """

    robotWidth = 0.01
    pyl.plot(pos.x, pos.y, color=color, marker='o', markersize=10)
    pyl.plot([pos.x, pos.x + robotWidth*math.cos(pos.theta)],
             [pos.y, pos.y + robotWidth*math.sin(pos.theta)],
             color=color,
             linewidth = 4)



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
    print(pygame.K_SPACE,c)
    return cok,c


def doRun():
    if State == "AvanceRapide" or state == "Recule" : motionProxy.stopMove()
    motionProxy.setWalkTargetVelocity(x, y, 0, frequency)
    print(">>>>>> action : run for 1 s")   # do some work
    sonarProxy.subscribe("myApplication")
    time.sleep(0.2)
    newKey,c = getKey(); # check if key pressed
    event = "Go"
    if obstacle() : event = "Obstacle"
    else :
        if c==pygame.K_SPACE:
            event="Wait"
        if c==pygame.K_d:
            event="TurnR"
        if c==pygame.K_q:
            event="TurnL"
        if c==pygame.K_UP:
            event="Go"
        if c==pygame.K_s:
            event="Stop"
        if c==pygame.K_qSHIFT:
            event = "Gofast"
        if c==pygame.K_DOWN:
            event = "MovingBackward"
    return event

def TurnRight():
    motionProxy.setWalkTargetVelocity(0, y, theta1, frequency)
    print(">>>>>> action : rotation a droite pendant 1 s") 
    time.sleep(0.2)
    newKey,c = getKey(); # check if key pressed
    event = "TurnR"
    if newKey:
        if c==pygame.K_SPACE:
            event="Wait"
        if c==pygame.K_q:
            event="TurnL"
        if c==pygame.K_UP:
            event="Go"
        if c==pygame.K_s:
            event="Stop"
        if c==pygame.K_qSHIFT:
            event = "Gofast"
        if c==pygame.K_DOWN:
            event = "MovingBackward"
    return event

def TurnLeft():
    motionProxy.setWalkTargetVelocity(0, y, theta2, frequency)
    print(">>>>>> action : rotation a gauche pendant 1 s") 
    time.sleep(0.2)
    newKey,c = getKey(); # check if key pressed
    event = "TurnL"
    if newKey:
        if c==pygame.K_SPACE:
            event="Wait"
        if c==pygame.K_d:
            event="TurnR"
        if c==pygame.K_UP:
            event="Go"
        if c==pygame.K_s:
            event="Stop"
        if c==pygame.K_qSHIFT:
            event = "Gofast"
        if c==pygame.K_DOWN:
            event = "MovingBackward"
    return event

def doWait():
    motionProxy.stopMove()
    time.sleep(0.2)
    newKey,c = getKey(); # check if key pressed
    event = "Wait"
    if newKey:
        if c==pygame.K_d:
            event="TurnR"
        if c==pygame.K_q:
            event="TurnL"
        if c==pygame.K_UP:
            event="Go"
        if c==pygame.K_s:
            event="Stop"
        if c==pygame.K_SPACE:
            event="Fonctionne"
        if c==pygame.K_b:
            event="Bed"
        if c==pygame.K_qSHIFT:
            event = "Gofast"
        if c==pygame.K_DOWN:
            event = "MovingBackward"
    return event

def doCrouch():
    postureProxy.goToPosture("Crouch", 0.3)
    motionProxy.setStiffnesses("Body", 0.0)
    print(">>>>>> action : sleep d'1 s")
    time.sleep(0.2)
    newKey,c = getKey(); # check if key pressed
    event = "Bed"
    if newKey:
        if c==pygame.K_s:
            event="Stop"
        if c==pygame.K_SPACE:
            event="Fonctionne"
    return event

def dofonctionne():
    postureProxy.goToPosture("StandInit", 0.5)
    motionProxy.setWalkArmsEnabled(True, True)
    print(">>>>>> action :Pret") 
    time.sleep(0.2)
    newKey,c = getKey(); # check if key pressed
    event = "Wait"
    if newKey:
        if c==pygame.K_SPACE:
            event="Wait"
        if c==pygame.K_d:
            event="TurnR"
        if c==pygame.K_UP:
            event="Go"
        if c==pygame.K_s:
            event="Stop"
        if c==pygame.K_b:
            event="Bed"
        if c==pygame.K_q:
            event="TurnL"
        if c==pygame.K_DOWN:
            event = "MovingBackward"
    return event

def doAvoid():
    X = 0.2
    global DD
    k = DD
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
    newKey,c = getKey()
    event = "Nothing"
    if obstacle() : event = "Obstacle"
    else :
        if c==pygame.K_SPACE:
            event="Wait"
        if c==pygame.K_d:
            event="TurnR"
        if c==pygame.K_UP:
            event="Go"
        if c==pygame.K_s:
            event="Stop"
        if c==pygame.K_b:
            event="Bed"
        if c==pygame.K_q:
            event="TurnL"
    return event

def obstacle():
    global DD
    # Get sonar left first echo (distance in meters to the first obstacle).
    le = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
    # Same thing for right.
    re = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
        # Get sonar left first echo (distance in meters to the first obstacle).
    time.sleep(0.1)
    le1 = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
    # Same thing for right.
    re1 = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
    seuil = 0.5
    if (re<seuil and re1<seuil) or (le<seuil and le1<seuil) or (le<seuil and re1<seuil) or (le1<seuil and re<seuil):
        if re1 < le1 : DD = 1
        else : DD = 0
        return True
    else:
        return False


def Stop():
    motionProxy.stopMove()
    postureProxy.goToPosture("Crouch", 0.3)
    motionProxy.setStiffnesses("Body", 0.0)
    print(">>>>>> Fin du programme") 
    return "Stop"

def doFast():
    motionProxy.setWalkTargetVelocity(1.0, 0, 0, 0.3)
    print(">>>>>> action : Avance Rapide pendant 1 s")
    time.sleep(1.0)
    newKey,c = getKey();
    event = "Gofast"
    if newKey:
        if c==pygame.K_d:
            event="TurnR"
        if c==pygame.K_q:
            event="TurnL"
        if c==pygame.K_UP:
            event="Go"
        if c==pygame.K_s:
            event="Stop"
        if c==pygame.K_SPACE:
            event="Wait"
        if c==pygame.K_b:
            event="Bed"
        if c==pygame.K_qSHIFT:
            event = "Gofast"
        if c==pygame.K_DOWN:
            event = "MovingBackward"
    return event


def doRecule():
    if State != "Recule" and State != "Ready" : motionProxy.stopMove()
    motionProxy.setWalkTargetVelocity(-1.0, 0, 0, 0.1)
    print(">>>>>> action : Recule pendant 1 s")
    time.sleep(1.0)
    newKey,c = getKey();
    event = "MovingBackward"
    if newKey:
        if c==pygame.K_d:
            event="TurnR"
        if c==pygame.K_q:
            event="TurnL"
        if c==pygame.K_s:
            event="Stop"
        if c==pygame.K_SPACE:
            event="Wait"
        if c==pygame.K_b:
            event="Bed"
        if c==pygame.K_DOWN:
            event = "MovingBackward"
    return event

if __name__== "__main__":
    
    # define the states
    f.add_state ("Idle")
    f.add_state ("Ready")
    f.add_state ("Deplacement")
    f.add_state ("Rotation")
    f.add_state ("End")
    f.add_state ("AvanceRapide")
    f.add_state ("Recule")
    f.add_state ("Avoid")


    # defines the events 
    f.add_event ("Wait")
    f.add_event ("Go")
    f.add_event ("TurnR")
    f.add_event ("TurnL")
    f.add_event ("Stop")
    f.add_event ("Fonctionne")
    f.add_event ("Bed")
    f.add_event ("Gofast")
    f.add_event ("MovingBackward")
    f.add_event ("Obstacle")
   
    # defines the transition matrix
    # current state, next state, event, action in next state
    f.add_transition ("Ready","Ready","Wait",doWait); # example
    f.add_transition ("Ready","Deplacement","Go",doRun);
    f.add_transition ("Ready","Rotation","TurnR",TurnRight);
    f.add_transition ("Ready","Rotation","TurnL",TurnLeft);
    f.add_transition ("Ready","End","Stop",Stop);
    f.add_transition ("Ready","Idle","Bed",doCrouch);
    f.add_transition ("Ready","AvanceRapide","Gofast",doFast);
    f.add_transition ("Ready","Recule","MovingBackward",doRecule);
    
    f.add_transition ("Rotation","Ready","Wait",doWait);
    f.add_transition ("Rotation","Rotation","TurnR",TurnRight);
    f.add_transition ("Rotation","Rotation","TurnL",TurnLeft);
    f.add_transition ("Rotation","End","Stop",Stop);
    f.add_transition ("Rotation","Deplacement","Go",doRun);
    f.add_transition ("Rotation","AvanceRapide","Gofast",doFast);
    f.add_transition ("Rotation","Recule","MovingBackward",doRecule);
    
    f.add_transition ("Deplacement","Deplacement","Go",doRun);
    f.add_transition ("Deplacement","Ready","Wait",doWait);
    f.add_transition ("Deplacement","Rotation","TurnL",TurnLeft);
    f.add_transition ("Deplacement","Rotation","TurnR",TurnRight);
    f.add_transition ("Deplacement","End","Stop",Stop);
    f.add_transition ("Deplacement","AvanceRapide","Gofast",doFast);
    f.add_transition ("Deplacement","Avoid","Obstacle",doAvoid)
    f.add_transition ("Deplacement","Recule","MovingBackward",doRecule)

    f.add_transition ("Idle","Ready","Fonctionne",dofonctionne);
    f.add_transition ("Idle","End","Stop",Stop);
    f.add_transition ("Idle","Idle","Bed",doCrouch);
    
    f.add_transition ("AvanceRapide","Ready","Wait",doWait);
    f.add_transition ("AvanceRapide","AvanceRapide","Gofast",doFast);
    f.add_transition ("AvanceRapide","Rotation","TurnR",TurnRight);
    f.add_transition ("AvanceRapide","Rotation","TurnL",TurnLeft);
    f.add_transition ("AvanceRapide","Deplacement","Go",doRun);
    f.add_transition ("AvanceRapide","End","Stop",Stop);
    f.add_transition ("AvanceRapide","Recule","MovingBackward",doRecule)
    
    f.add_transition ("Recule","Recule","MovingBackward",doRecule);
    f.add_transition ("Recule","Ready","Wait",doWait);
    f.add_transition ("Recule","Deplacement","Go",doRun);
    f.add_transition ("Recule","Rotation","TurnR",TurnRight);
    f.add_transition ("Recule","Rotation","TurnL",TurnLeft);
    f.add_transition ("Recule","End","Stop",Stop);

    f.add_transition ("Avoid","Avoid","Obstacle",doAvoid)
    f.add_transition("Avoid","Deplacement","Nothing",doRun)
    f.add_transition("Avoid","Idle","Bed",doCrouch)
    f.add_transition("Avoid","Ready","Wait",doWait)
    f.add_transition ("Avoid","Rotation","TurnL",TurnLeft);
    f.add_transition ("Avoid","Rotation","TurnR",TurnRight);
    f.add_transition ("Avoid","End","Stop",Stop);
    
    # initial state
    f.set_state ("Idle") # ... replace with your initial state
    # first event
    f.set_event ("Bed") # ...  replace with you first event 
    # end state
    end_state = "End" # ... replace  with your end state

 
    # fsm loop
    run = True   
    while (run):
        State = f.curState
        funct = f.run () # function to be executed in the new state
        if f.curState != end_state:
            newEvent = funct() # new event when state action is finished
            print("New Event : ",newEvent)
            f.set_event(newEvent) # set new event for next transition
        else:
            funct()
            run = False
            
    print("End of the programm")



