# -*- coding: utf-8 -*-
import fsm
import time
import sys
import select 
import pygame
from pygame.locals import *
import motion
from naoqi import ALProxy
import math
import numpy as np
import naocmd as cm

pygame.init()
fenetre = pygame.display.set_mode((489,709), RESIZABLE)
fond = pygame.image.load("terrain-de-football.jpg").convert()
fenetre.blit(fond, (0,0))
arrow = pygame.image.load("fleche.png")
arrow_rot_l = pygame.image.load("fleche_rot_l.png")
arrow_rot_r = pygame.image.load("fleche_rot_r.png")
perso = pygame.image.load("robot_nao.png").convert_alpha()

fenetre.blit(perso, (190,260))
#pygame.display.set_mode((100,  100))

try :
    pygame.joystick.init()
    joy = pygame.joystick.Joystick(0)
    joy.init()
except:
    print "Could not find joystick"

# global variables
f = fsm.fsm();  # finite state machine
tseq= 0.5
fractSpeed=0.8
global is_sleeping
is_sleeping = False

P = 0.5
TP = 0.25

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
    fenetre.blit(fond, (0,0))
    fenetre.blit(perso, (190,260))
    pygame.display.flip()
    global is_sleeping
    global event
    if is_sleeping == False:
        postureProxy.goToPosture("Crouch", fractSpeed)
        time.sleep(tseq/2)
        motionProxy.setStiffnesses("Body", 0.0)
        #tts.say("Tuer tous les humains ! Tuer tous les humain !")
    event="Stay" # define the default event
    is_sleeping = True
    time.sleep(tseq/2)
    for even in pygame.event.get():
        if even.type == pygame.QUIT:
            sys.exit()
        if even.type == pygame.KEYDOWN:
            if even.key == pygame.K_s:
                event="Start"
                cm.IDLEtoReady()
        elif even.type == pygame.JOYBUTTONDOWN:
            if joy.get_button(1) == 1:
                event="Start"
    return event

def possibilityStart():
    fenetre.blit(fond, (0,0))
    fenetre.blit(perso, (190,260))
    pygame.display.flip()
    global is_sleeping
    global event
    is_sleeping = False
    motionProxy.setStiffnesses("Body", 1.0)
    X = 0.0
    Y = 0.0
    Theta = 0.0
    Frequency = 0.8
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency) # do some work # do some work
    postureProxy.goToPosture("StandInit", fractSpeed)
    time.sleep(tseq)
    #procédure évitement
    if event == "StopMoveA":
        event = "MoveBackwardA"
        cm.AlltoBK()
    elif event == "StopMoveAR":
        #Rajouter compteur au bsn
        event = "RotateRightA"
        cm.ReadytoRD()
    elif event == "StopMoveAL":
        event = "RotateLeftA"
        cm.ReadytoRG()
    elif event == "StopRotateA" or event == "StopMoveAF":
        event = "MoveForward"
        cm.ReadytoAvance()
    else: 
        event="Stay" 
        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                sys.exit()
            if even.type == pygame.KEYDOWN:
                if even.key == pygame.K_UP:
                    event="MoveForward"
                    cm.ReadytoAvance()
                elif even.key == pygame.K_DOWN:
                    event="MoveBackward" 
                    cm.AlltoBK()
                elif even.key == pygame.K_LEFT:
                    event="RotateLeft"
                    cm.ReadytoRG()
                elif even.key == pygame.K_RIGHT:
                    event="RotateRight" 
                    cm.ReadytoRD()
                elif even.key == pygame.K_p:
                    event="Pause" 
                    cm.ReadytoIDLE()
                elif even.key == pygame.K_k:
                    event="Kill"    
                elif even.key == pygame.K_SPACE:
                    event="Shoot"   
                elif even.key == pygame.K_d:
                    event="Dab"  
            if even.type == pygame.JOYAXISMOTION:
                if joy.get_axis(1) < 0 :
                    event="MoveForward"
                elif joy.get_axis(1) > 0:
                    event="MoveBackward" 
                elif joy.get_axis(0) < 0 :
                    event="RotateLeft"
                elif joy.get_axis(0) > 0 :
                    event="RotateRight"
            if even.type == pygame.JOYBUTTONDOWN:
                if joy.get_button(2) == 1:
                    event="Pause" 
                elif joy.get_button(6) == 1:
                    event="Kill"    
                elif joy.get_button(0) == 1:
                    event="Shoot"  
                elif joy.get_button(9) ==1:
                    event = "Dab"
    return event

def possibilityStop():
    global is_sleeping
    global event
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
    sys.exit()
    return event

def possibilityForward():
    global event
    X = 0.5
    Y = 0.0
    Theta = 0.0
    Frequency = 0.8
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency) # do some work
    time.sleep(tseq)
    fenetre.blit(fond, (0,0))
    fenetre.blit(perso, (190,260))
    arrow_up = pygame.transform.rotate(arrow, 90)
    fenetre.blit(arrow_up, (110,0))
    pygame.display.flip()
    
    event="Stay" # define the default event
    
    # Modification des méthodes d'esquives automatiques;    
    sonarProxy.subscribe("SonarApp");
    time.sleep(0.25)
    valL = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
    print("a gauche, mon sonar detecte", valL)
    valR = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
    print("a droite, mon sonar detecte", valR)
    sonarProxy.unsubscribe("SonarApp");

    if valL <= TP and valR <= TP:
        print("Objets tres proches droit devant")
        event = "StopMoveA"
        #MOD
    elif valL <= TP:
        print("objet tres proche a ma gauche")
        event = "StopMoveAR"
    elif valR <= TP:
        print("objet tres proche a ma droite")
        event = "StopMoveAL"
    elif valL <= P:
        print("objet proche a ma gauche")
        event = "RotateRightA"
        cm.ReadytoRD()
    elif valR <= P:
        print("objet proche a ma droite")
        event = "RotateLeftA"   
        cm.ReadytoRG()
    
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
                cm.ReadytoRG()
            elif even.key == pygame.K_RIGHT:
                event="RotateRight" 
                cm.ReadytoRD()
        if even.type == pygame.JOYAXISMOTION:
            if joy.get_axis(1) > 0:
                event="StopMove"
            elif joy.get_axis(0) < 0:
                event="RotateLeft"
            elif joy.get_axis(0) > 0:
                event="RotateRight" 
        elif even.type == pygame.JOYBUTTONDOWN:
            if joy.get_button(7) == 1:
                event="StopMove"
    return event # return event to be able to define the transition

def possibilityBackward():
    fenetre.blit(fond, (0,0))
    fenetre.blit(perso, (190,260))
    arrow_down = pygame.transform.rotate(arrow, -90)
    fenetre.blit(arrow_down, (110,450))
    pygame.display.flip()
    global event
    X = -0.5
    Y = 0.0
    Theta = 0.0
    Frequency = 0.8
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency) # do some work
    time.sleep(tseq)
    
    if event == "MoveBackwardA":
        sonarProxy.subscribe("SonarApp");
        time.sleep(0.25)
        valL = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
        print("a gauche, mon sonar detecte", valL)
        valR = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
        print("a droite, mon sonar detecte", valR)
        sonarProxy.unsubscribe("SonarApp");
        if min(valL,valR) > TP:
            event = "StopMoveAF"
        for even in pygame.event.get():
            if even.type == pygame.KEYDOWN:
                event = "Stay"
    else :
        event="Stay" # define the default event
        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                sys.exit()
            if even.type == pygame.KEYDOWN:
                if even.key == pygame.K_s:
                    event="StopMove"
                elif even.key == pygame.K_LEFT:
                    event="RotateLeft"
                elif even.key == pygame.K_RIGHT:
                    event="RotateRight"
                elif even.key == pygame.K_UP:
                    event="StopMove"
            if even.type == pygame.JOYBUTTONDOWN:
                if joy.get_button(7) == 1:
                    event="StopMove"
            elif even.type == pygame.JOYAXISMOTION :
                if joy.get_axis(0) < 0:
                    event="RotateLeft"
                elif joy.get_axis(0) > 0:
                    event="RotateRight"
                elif joy.get_axis(1) < 0:
                    event="StopMove"
    return event # return event to be able to define the transition

def possibilityRight():
    fenetre.blit(fond, (0,0))
    fenetre.blit(perso, (190,260))
    arrow_right = pygame.transform.scale(arrow_rot_r, (300, 300))
    fenetre.blit(arrow_right, (100,220))
    pygame.display.flip()
    global event
    X = 0.0
    Y = 0.0
    Theta = -0.5
    Frequency = 0.8
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)  # do some work
    time.sleep(tseq)
    if event == "RotateRightA":
        sonarProxy.subscribe("SonarApp");
        time.sleep(0.25)
        valL = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
        print("a gauche, mon sonar detecte", valL)
        valR = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
        print("a droite, mon sonar detecte", valR)
        sonarProxy.unsubscribe("SonarApp");
        if valL > TP:
            event = "StopRotateA"       
        for even in pygame.event.get():
            if even.type == pygame.KEYDOWN:
                event = "Stay"
    event="Stay" # define the default event
    for even in pygame.event.get():
        if even.type == pygame.QUIT:
            sys.exit()
        if even.type == pygame.KEYDOWN:
            if even.key == pygame.K_s:
                event="StopRotate"
            elif even.key == pygame.K_UP:
                event="MoveForward"
                cm.ReadytoAvance()
            elif even.key == pygame.K_DOWN:
                event="MoveBackward"  
                cm.AlltoBK()
            elif even.key == pygame.K_LEFT:
                event="StopRotate"
        if even.type == pygame.JOYBUTTONDOWN:
            if joy.get_button(7) == 1:
                event="StopRotate"
        elif even.type == pygame.JOYAXISMOTION :
            if joy.get_axis(1) < 0:
                event="MoveForward"
            elif joy.get_axis(1) > 0:
                event="MoveBackward"
            elif joy.get_axis(0) < 0:
                event="StopRotate"
    return event

def possibilityLeft():
    fenetre.blit(fond, (0,0))
    fenetre.blit(perso, (190,260))
    arrow_left = pygame.transform.scale(arrow_rot_l, (300, 300))
    fenetre.blit(arrow_left, (100,220))
    pygame.display.flip()
    global event
    X = 0.0
    Y = 0.0
    Theta = 0.5
    Frequency = 0.8
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency) # do some work
    time.sleep(tseq)
    if event == "RotateLeftA":
        sonarProxy.subscribe("SonarApp");
        time.sleep(0.25)
        valL = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
        print("a gauche, mon sonar detecte", valL)
        valR = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
        print("a droite, mon sonar detecte", valR)
        sonarProxy.unsubscribe("SonarApp");
        if valR > TP:
            event = "StopRotateA"
        for even in pygame.event.get():
            if even.type == pygame.KEYDOWN:
              event = "Stay"
    else:
        event="Stay" # define the default event
        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                sys.exit()
            if even.type == pygame.KEYDOWN:
                if even.key == pygame.K_s:
                    event="StopRotate"
                elif even.key == pygame.K_UP:
                    event="MoveForward"
                    cm.ReadytoAvance()
                elif even.key == pygame.K_DOWN:
                    event="MoveBackward"  
                    cm.AlltoBK()  
                elif even.key == pygame.K_RIGHT:
                    event="StopRotate"
            if even.type == pygame.JOYBUTTONDOWN:
                if joy.get_button(7) == 1:
                    event="StopRotate"
            elif even.type == pygame.JOYAXISMOTION :
                if joy.get_axis(1) < 0:
                    event="MoveForward"
                elif joy.get_axis(1) > 0:
                    event="MoveBackward"
                elif joy.get_axis(0) > 0:
                    event="StopRotate"
    return event

def possibilityBackwardLeft():
    fenetre.blit(fond, (0,0))
    fenetre.blit(perso, (190,260))
    arrow_dbl = pygame.transform.rotate(arrow, -140)
    arrow_dbl = pygame.transform.scale(arrow_dbl, (150, 300))
    arrow_dbl.set_colorkey((255,255,255))
    fenetre.blit(arrow_dbl, (70,370))
    pygame.display.flip()
    global event
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
            elif even.key == pygame.K_DOWN:
                event="StopRotate" 
                cm.AlltoBK()
            elif even.key == pygame.K_LEFT:
                event="StopMove"
                cm.ReadytoRG()
            elif even.key == pygame.K_UP:
                event="StopMove"
            elif even.key == pygame.K_RIGHT:
                event="StopRotate" 
                cm.AlltoBK()
        if even.type == pygame.JOYBUTTONDOWN:
            if joy.get_button(7) == 1:
                event="Stop"
        elif even.type == pygame.JOYAXISMOTION :
            if joy.get_axis(1) < 0:
                event="StopMove"
            elif joy.get_axis(0) > 0:
                event="StopRotate"
    return event # return event to be able to define the transition

def possibilityBackwardRight():
    fenetre.blit(fond, (0,0))
    fenetre.blit(perso, (190,260))
    arrow_dbl = pygame.transform.rotate(arrow, -40)
    arrow_dbl = pygame.transform.scale(arrow_dbl, (150, 300))
    arrow_dbl.set_colorkey((255,255,255))
    fenetre.blit(arrow_dbl, (250,370))
    pygame.display.flip()
    global event
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
            elif even.key == pygame.K_DOWN:
                event="StopRotate" 
                cm.AlltoBK()
            elif even.key == pygame.K_RIGHT:
                event="StopMove" 
                cm.ReadytoRD()
            elif even.key == pygame.K_LEFT:
                event="StopRotate"
                cm.AlltoBK()
            elif even.key == pygame.K_UP:
                event="StopMove"
        if even.type == pygame.JOYBUTTONDOWN:
            if joy.get_button(7) == 1:
                event="Stop"
        elif even.type == pygame.JOYAXISMOTION :
            if joy.get_axis(1) < 0:
                event="StopMove"
            elif joy.get_axis(0) < 0:
                event="StopRotate"
    return event # return event to be able to define the transition

def possibilityForwardLeft():
    fenetre.blit(fond, (0,0))
    fenetre.blit(perso, (190,260))
    arrow_dbl = pygame.transform.rotate(arrow, 140)
    arrow_dbl = pygame.transform.scale(arrow_dbl, (150, 300))
    arrow_dbl.set_colorkey((255,255,255))
    fenetre.blit(arrow_dbl, (70,70))
    pygame.display.flip()
    global event
    X = 0.5
    Y = 0.0
    Theta = 0.5
    Frequency = 0.8
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency) # do some work
    time.sleep(tseq)
    if event == "RotateLeftA":
        sonarProxy.subscribe("SonarApp")
        time.sleep(0.25)
        valL = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
        print("a gauche, mon sonar detecte", valL)
        valR = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
        print("a droite, mon sonar detecte", valR)
        sonarProxy.unsubscribe("SonarApp");
        if valR > P or valR <= TP:
            event = "StopRotate"
        if valL < valR:
            event = "RotateRightA"
            cm.ReadytoRD()
        for even in pygame.event.get():
            if even.type == pygame.KEYDOWN:
               event = "Stay"
    else :
        event="Stay" # define the default event
        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                sys.exit()
            if even.type == pygame.KEYDOWN:
                if even.key == pygame.K_s:
                    event="Stop"
                elif even.key == pygame.K_UP:
                    event="StopRotate" 
                elif even.key == pygame.K_LEFT:
                    event="StopMove" 
                elif even.key == pygame.K_DOWN:
                    event="StopMove" 
                elif even.key == pygame.K_RIGHT:
                    event="StopRotate" 
            if even.type == pygame.JOYBUTTONDOWN:
                if joy.get_button(7) == 1:
                    event="Stop"
            elif even.type == pygame.JOYAXISMOTION :
                if joy.get_axis(1) > 0:
                    event="StopMove"
                elif joy.get_axis(0) > 0:
                    event="StopRotate"
    return event # return event to be able to define the transition

def possibilityForwardRight():
    fenetre.blit(fond, (0,0))
    fenetre.blit(perso, (190,260))
    arrow_dbl = pygame.transform.rotate(arrow, 40)
    arrow_dbl = pygame.transform.scale(arrow_dbl, (150, 300))
    arrow_dbl.set_colorkey((255,255,255))
    fenetre.blit(arrow_dbl, (250,70))
    pygame.display.flip()
    global event
    X = 0.5
    Y = 0.0
    Theta = -0.5
    Frequency = 0.8
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency) # do some work
    time.sleep(tseq)
    if event == "RotateRightA":
        sonarProxy.subscribe("SonarApp")
        time.sleep(0.25)
        valL = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
        print("a gauche, mon sonar detecte", valL)
        valR = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
        print("a droite, mon sonar detecte", valR)
        sonarProxy.unsubscribe("SonarApp");
        if valL > P or valL <= TP:
            event = "StopRotate"
        if valR < valL:
            event = "RotateLeftA"
            cm.ReadytoRG()
        for even in pygame.event.get():
            if even.type == pygame.KEYDOWN:
                event = "Stay"
    else :
        event="Stay" # define the default event
        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                sys.exit()
            if even.type == pygame.KEYDOWN:
                if even.key == pygame.K_s:
                    event="Stop"
                elif even.key == pygame.K_UP:
                    event="StopRotate" 
                elif even.key == pygame.K_RIGHT:
                    event="StopMove" 
                elif even.key == pygame.K_DOWN:
                    event="StopMove" 
                elif even.key == pygame.K_LEFT:
                    event="StopRotate" 
            if even.type == pygame.JOYBUTTONDOWN:
                if joy.get_button(7) == 1:
                    event="Stop"
            elif even.type == pygame.JOYAXISMOTION :
                if joy.get_axis(1) > 0:
                    event="StopMove"
                elif joy.get_axis(0) < 0:
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
  dx      = 0.15               # translation axis X (meters)
  dz      = 0.05             # translation axis Z (meters)
  dwy     = 2.0*math.pi/180.0    # rotation axis Y (radian)
  times   = [1.5, 1.9, 3.0]
  isAbsolute = False
  targetList = [
    [-0.00, 0.0, dz, 0.0, +dwy, 0.0],
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

def doDab():
    jointName = "HeadPitch";
    stiffness = 1.0
    Hd1 = [30]
    Hd1 = [ x * motion.TO_RAD for x in Hd1]
    
    JointNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll"]
    JointNames2 = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]
    Arm1 = [-30,  -60, 0, -50]
    Arm1 = [ x * motion.TO_RAD for x in Arm1]
    Arm2 = [-50,  -40, 0, -80]
    Arm2 = [ x * motion.TO_RAD for x in Arm2]

    pFractionMaxSpeed = 0.6
    motionProxy.post.angleInterpolationWithSpeed(JointNames, Arm1, pFractionMaxSpeed)
    motionProxy.post.angleInterpolationWithSpeed(JointNames2, Arm2, pFractionMaxSpeed)
    motionProxy.post.angleInterpolationWithSpeed(jointName, Hd1, 0.2)
    time.sleep(2.0)
    motionProxy.angleInterpolationWithSpeed(jointName, 0, 0.2)

    time.sleep(2.0)
    event="Stop"
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
    f.add_state ("Dab")

    # defines the events 
    f.add_event ("Launch")
    f.add_event ("MoveForward")
    f.add_event ("MoveBackward")
    f.add_event ("MoveBackwardA")
    f.add_event ("RotateLeft")
    f.add_event ("RotateRight")
    f.add_event ("RotateLeftA")
    f.add_event ("RotateRightA")
    f.add_event ("Kill")
    f.add_event ("StopMoveAR")
    f.add_event ("StopMoveAF")
    f.add_event ("StopMove")
    f.add_event ("StopMoveAL")
    f.add_event ("StopRotateA")
    
    f.add_event ("Pause")
    f.add_event ("Stay")
    f.add_event ("Stop")
    f.add_event ("Shoot")
    f.add_event ("Dab")
    
    # defines the transition matrix
    # current state, next state, event, action in next state
    f.add_transition ("Idle","Idle","Stay",possibilityIdle);
    f.add_transition ("Start","Start","Stay",possibilityStart);
    f.add_transition ("Stop","Stop","Stay",possibilityStop);
    
    f.add_transition ("Idle","Start","Start",possibilityStart);
    f.add_transition ("Start","Forward","MoveForward",possibilityForward);
    f.add_transition ("Start","Backward","MoveBackward",possibilityBackward);
    f.add_transition ("Start","Backward","MoveBackwardA",possibilityBackward);
    f.add_transition ("Forward","Forward","Stay",possibilityForward);
    f.add_transition ("Backward","Backward","Stay",possibilityBackward);
    f.add_transition ("Backward","Backward","MoveBackwardA",possibilityBackward);
    f.add_transition ("Forward","Start","StopMove",possibilityStart);
    f.add_transition ("Forward","Start","StopMoveA",possibilityStart);
    f.add_transition ("Forward","Start","StopMoveAR",possibilityStart);
    f.add_transition ("Forward","Start","StopMoveAL",possibilityStart);
    f.add_transition ("Backward","Start","StopMove",possibilityStart);
    f.add_transition ("Backward","Start","StopMoveAF",possibilityStart);
    
    f.add_transition ("Start","Left","RotateLeft",possibilityLeft);
    f.add_transition ("Start","Left","RotateLeftA",possibilityLeft);
    f.add_transition ("Start","Right","RotateRight",possibilityRight);
    f.add_transition ("Start","Right","RotateRightA",possibilityRight);
    
    f.add_transition ("Left","Left","Stay",possibilityLeft);
    f.add_transition ("Left","Left","RotateLeftA",possibilityLeft);
    f.add_transition ("Right","Right","Stay",possibilityRight);
    f.add_transition ("Right","Right","RotateRightA",possibilityRight);
    f.add_transition ("Left","Start","StopRotate",possibilityStart);
    f.add_transition ("Right","Start","StopRotate",possibilityStart);
    f.add_transition("ForwardRight","ForwardLeft","RotateLeftA",possibilityForwardLeft)
    f.add_transition("ForwardLeft","ForwardRight","RotateRightA",possibilityForwardRight)
    
    f.add_transition ("Left","Start","StopRotateA",possibilityStart);
    f.add_transition ("Right","Start","StopRotateA",possibilityStart);
    
    f.add_transition ("Start","Idle","Pause",possibilityIdle);
    f.add_transition ("Start","Stop","Kill",possibilityStop);
    
    f.add_transition ("ForwardLeft","ForwardLeft","Stay",possibilityForwardLeft);
    f.add_transition ("ForwardLeft","ForwardLeft","RotateLeftA",possibilityForwardLeft);
    f.add_transition ("ForwardRight","ForwardRight","RotateRightA",possibilityForwardRight);    
    f.add_transition ("ForwardRight","ForwardRight","Stay",possibilityForwardRight);
    f.add_transition ("BackwardLeft","BackwardLeft","Stay",possibilityBackwardLeft);
    f.add_transition ("BackwardRight","BackwardRight","Stay",possibilityBackwardRight);
    
    f.add_transition ("Forward","ForwardLeft","RotateLeft",possibilityForwardLeft);
    f.add_transition ("Forward","ForwardRight","RotateRight",possibilityForwardRight);
    f.add_transition ("Backward","BackwardLeft","RotateLeft",possibilityBackwardLeft);
    f.add_transition ("Backward","BackwardRight","RotateRight",possibilityBackwardRight);
    
    f.add_transition ("Forward","ForwardLeft","RotateLeftA",possibilityForwardLeft);
    f.add_transition ("Forward","ForwardRight","RotateRightA",possibilityForwardRight);
    f.add_transition ("ForwardLeft","ForwardLeft","RotateLeftA",possibilityForwardLeft);
    f.add_transition ("ForwardRight","ForwardRight","RotateRightA",possibilityForwardRight);
    
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
    
    f.add_transition ("Start","Shoot","Shoot",doShoot);
    f.add_transition ("Shoot","Start","Stay",possibilityStart);
    
    f.add_transition ("Start","Dab","Dab",doDab);
    f.add_transition ("Dab","Start","Stop",possibilityStart);
    
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



