import sys
import motion
import time
from naoqi import ALProxy
import math


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

squareSideLength = 1.0  # square of 50 cm sides
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



# Set NAO in Stiffness On 
# using wakeUp (new feature in 1.14.1)
motionProxy.wakeUp()


# Send NAO to Pose Init : it not standing then standing up
postureProxy.goToPosture("StandInit", 0.5)

# Enable arms control by Walk algorithm
motionProxy.setWalkArmsEnabled(True, True)

# allow to stop motion when losing ground contact, NAO stops walking
# when lifted  (True is default)
motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])


for iloop in range (4):

    voicePxy.say("Side %d"%(iloop+1))

    # turn 90 degrees clockwise (in place)
    x = 0.2
    y = 0.0
    theta = -math.pi/2.0
    motionProxy.moveTo (x, y, theta)
    print "Side %d"%(iloop+1)

    # go forward
    x = squareSideLength
    y = 0.0
    theta = 0.0
    motionProxy.moveTo (x, y, theta)

# End Walk (putting NAO at rest position to save power)
motionProxy.rest()
