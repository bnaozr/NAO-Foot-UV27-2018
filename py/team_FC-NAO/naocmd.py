import sys
import motion
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

    return(motionProxy,postureProxy,sonarProxy, memoryProxy)



def tout_droit(motion,posture,freq):
    motion.stopMove()
    x  = 1.0
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

