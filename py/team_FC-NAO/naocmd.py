import sys
import motion as mo
import time
from naoqi import ALProxy
import math

def initialisation():
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
        memoryProxy = ALProxy("ALMemory", robotIp, robotPort)
    except Exception, e:
        print "Could not create proxy to ALMemory"
        print "Error was: ", e

    try:
        sonarProxy = ALProxy("ALSonar", robotIp, robotPort)
    except Exception, e:
        print "Could not create proxy to ALSonar"
        print "Error was: ", e

    motionProxy.wakeUp()
    motionProxy.setStiffnesses("Body", 1.0)

    return(motionProxy,postureProxy,sonarProxy,memoryProxy)

def decal_droite(motion,posture,freq):
    motion.stopMove()
    x  = 0.0
    y  = -1.0
    theta  = 0.0
    motion.setWalkTargetVelocity(x, y, theta, freq)
    
def decal_gauche(motion,posture,freq):
    motion.stopMove()
    x  = 0.0
    y  = 1.0
    theta  = 0.0
    motion.setWalkTargetVelocity(x, y, theta, freq)

def tout_droit(motion,posture,freq,x,y):
    motion.stopMove()
    theta  = 0.0
    motion.setWalkTargetVelocity(x, y, theta, freq)

def marche_arriere(motion,posture,freq):
    motion.stopMove()
    x  = -1.0
    y  = 0.0
    theta  = 0.0
    motion.setWalkTargetVelocity(x, y, theta, freq)
    
def tourner_a_gauche(motion,freq):
    motion.stopMove()
    x  = 0.0
    y  = 0.0
    theta  = 1.0
    motion.setWalkTargetVelocity(x, y, theta, freq)

def tourner_a_droite(motion,freq):
    motion.stopMove()
    x  = 0.0
    y  = 0.0
    theta  = -1.0
    motion.setWalkTargetVelocity(x, y, theta, freq)

def tir(motion, posture, freq):

    posture.goToPosture("StandInit", 0.5)

    # Activate Whole Body Balancer
    isEnabled  = True
    motion.wbEnable(isEnabled)

    # Legs are constrained fixed
    stateName  = "Fixed"
    supportLeg = "Legs"
    motion.wbFootState(stateName, supportLeg)

    # Constraint Balance Motion
    isEnable   = True
    supportLeg = "Legs"
    motion.wbEnableBalanceConstraint(isEnable, supportLeg)

    # Com go to LLeg
    supportLeg = "LLeg"
    duration   = 2.0
    motion.wbGoToBalance(supportLeg, duration)

    motion.stopMove()
    stateName  = "Free"
    supportLeg = "RLeg"
    motion.wbFootState(stateName, supportLeg)
    effectorName = "RLeg"
    axisMask     = 63
    espace        = mo.FRAME_ROBOT
    dx      = 0.05                 
    dz      = 0.05                 
    dwy     = 5.0*math.pi/180.0    
    times   = [2.0, 3.7, 4.5]
    isAbsolute = False

    targetList = [[-dx, 0.0, dz, 0.0, +dwy, 0.0],[+dx, 0.0, dz, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

    motion.positionInterpolation(effectorName, espace, targetList,axisMask, times, isAbsolute)
    motion.stopMove()

def stop(motion):
    motion.stopMove()


def fin(motion,posture,fractSpeed=0.3):
    posture.goToPosture("Crouch", fractSpeed)
    motion.setStiffnesses("Body", 0.0)#Debloque les servo-moteurs

def donnee_sonar(sonar,memory,motion,dist=0.5):
    sonar.subscribe("SonarApp")
    time.sleep(0.1)
    valL = memory.getData("Device/SubDeviceList/US/Left/Sensor/Value")
    valR = memory.getData("Device/SubDeviceList/US/Right/Sensor/Value")
    if valL<dist or valR<dist:
        return True,valL,valR
    else:
        return False,valL,valR




if __name__=="__main__":
    motion,posture,sonar,memory=initialisation()
    tout_droit(motion,posture,1)
    time.sleep(5)
    tourner_a_gauche(motion,1)
    time.sleep(5)
    tourner_a_droite(motion,1)
    time.sleep(5)
    stop(motion)
    time.sleep(15)
    tourner_a_droite(motion,1)

