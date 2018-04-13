# -*- coding: utf-8 -*-
from naoqi import ALProxy


class Nao:
    def __init__(self, ip, port):
        self.motion = ALProxy('ALMotion', ip, int(port))
        self.sonar = ALProxy('ALSonar', ip, int(port))
        self.memory = ALProxy('ALMemory', ip, int(port))

        self.sonar.subscribe('nao')

        self.motion.wakeUp()

    def avoid_obstacle(self):
        d_left = self.memory.getData(
                "Device/SubDeviceList/US/Left/Sensor/Value")
        d_right = self.memory.getData(
                "Device/SubDeviceList/US/Right/Sensor/Value")

        if d_left < 0.3 or d_right < 0.3:
            self.standby()

    def get_pos(self):
        return self.motion.getRobotPosition(True)
	
	  #fonction de transitions en doNomévénement

    def doQuit(self):
        self.motion.stopMove()
        self.motion.rest()
		
    def doRight(self):
        self.motion.move(0, 0, -0.2)

    def doLeft(self):
		    self.motion.move(0, 0, 0.2)
		
    def doSleep(self):
		    self.motion.rest()

    def doStandby(self):
		    self.motion.stopMove()
		
    def doGo(self):
		    self.motion.move(0.1, 0, 0)
	
    def doGoback(self):
		    self.motion.move(-0.1, 0, 0)
	
    def doShoot(self):
		    self.motion.stopMove()

    def doWakeUp(self):
        self.motion.wakeUp()
	
	
