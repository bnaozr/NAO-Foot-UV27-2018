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

        if d_left < 0.5:
            self.wait()
            self.turn_right()

        elif d_right < 0.5:
            self.wait()
            self.turn_left()

    def crouch(self):
        self.motion.rest()

    def get_pos(self):
        return self.motion.getRobotPosition(True)

    def on_right_detected(self, **args):
        pass

    def rotate_left(self):
        self.motion.move(0, 0, 0.2)

    def rotate_right(self):
        self.motion.move(0, 0, -0.2)

    def stop_move(self):
        self.motion.stopMove()

    def walk(self):
        self.motion.move(0.1, 0, 0)

    def wake_up(self):
        self.motion.wakeUp()

    def walk_back(self):
        self.motion.move(-0.1, 0, 0)
