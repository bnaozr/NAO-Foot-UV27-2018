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

        if d_left < 0.3:
            self.wait()
            self.turn_right()

        elif d_right < 0.3:
            self.wait()
            self.turn_left()

    def crouch(self):
        self.motion.rest()

    def get_pos(self):
        return self.motion.getRobotPosition(True)


    def rotate_left(self):
        self.motion.move(0, 0, 0.2)

    

    def stop_move(self):
        self.motion.stopMove()

    def walk(self):
        self.motion.move(0.1, 0, 0)

    def wake_up(self):
        self.motion.wakeUp()

    def walk_back(self):
        self.motion.move(-0.1, 0, 0)
	
	#fonction de transitions en doNomévénement
	
	def doQuit(self):
		pass
		
	def doRight(self):
        self.motion.move(0, 0, -0.2)
		
	def doLeft(self):
		pass
		
	def doSleep(self):
		pass
	
	def doStop(self):
		pass
		
	def doGo(self):
		pass
	
	def doGoback(self):
		pass
	
	def doShoot(self):
		pass
	
	