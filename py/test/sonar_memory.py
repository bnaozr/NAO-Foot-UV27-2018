import sys
import motion
import time
from naoqi import ALProxy
import math

# test program to get NAO's left and right sonars (9999.0 if nothing, max range 1.5 m)
# this is the easy way to use sonars

robotIp="172.20.26.29"
robotIp="172.20.11.241"
robotPort=9559
robotIp="localhost"
robotPort=11212

if (len(sys.argv) >= 2):
    robotIp = sys.argv[1]
if (len(sys.argv) >= 3):
    robotPort = int(sys.argv[2])

#print robotIp
#print robotPort

# Init proxies.

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

for i in range(20):
    sonarProxy.subscribe("SonarApp");
    time.sleep(0.25)
    valL = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
    valR = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
    print valL, valR
    sonarProxy.unsubscribe("SonarApp");
    time.sleep(1.0-0.25)

