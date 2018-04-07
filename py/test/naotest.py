import sys
import motion
import time
from naoqi import ALProxy
import math


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

motionProxy.wakeUp()
motionProxy.setStiffnesses("Body", 1.0)

time_wait=3.0

fractSpeed=0.5
postureProxy.goToPosture("StandZero", fractSpeed)
time.sleep(time_wait)

postureProxy.goToPosture("StandInit", fractSpeed)
time.sleep(time_wait)

postureProxy.goToPosture("Sit", fractSpeed)
time.sleep(time_wait)

postureProxy.goToPosture("LyingBack", fractSpeed)
time.sleep(time_wait)

postureProxy.goToPosture("Crouch", fractSpeed)
time.sleep(time_wait)


motionProxy.setStiffnesses("Body", 0.0)
motionProxy.rest()
