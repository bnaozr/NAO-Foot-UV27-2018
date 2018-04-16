# -*- coding: utf-8 -*-
from naoqi import ALProxy
import sys
import motion
import time
import math
import numpy as np


class Nao:
    def __init__(self, ip, port):
        self.motion = ALProxy('ALMotion', ip, int(port))
        self.sonar = ALProxy('ALSonar', ip, int(port))
        self.memory = ALProxy('ALMemory', ip, int(port))
        self.postureProxy = ALProxy("ALRobotPosture", ip, int(port))
        self.sonar.subscribe('nao')
        self.tts = ALProxy("ALTextToSpeech", ip, int(port))

        self.maxXSpeed = 0.2
        self.maxYSpeed = 0.2
        self.maxRotationSpeed = 0.4
        self.xSpeed = 0
        self.ySpeed = 0
        self.rotationSpeed = 0

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

    # commandes au joystick
    def set_rotation_speed(self, rotationSpeed):
        self.rotationSpeed = rotationSpeed*self.maxRotationSpeed

    def set_x_speed(self, xSpeed):
        self.xSpeed = xSpeed*self.maxXSpeed

    def set_y_speed(self, ySpeed):
        self.ySpeed = ySpeed*self.maxYSpeed

    def doJoyMove(self):
        self.motion.move(self.xSpeed, self.ySpeed, self.rotationSpeed)

    # fonction de transitions en doNomévénement

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

    def walk_back(self):
        self.motion.move(-0.1, 0, 0)

    def sidestepR(self):
        footStepsList = []
        footStepsList.append([["RLeg"], [[0.00, -0.16, 0.0]]])
        footStepsList.append([["LLeg"], [[0.00, 0.1, 0.0]]])
        stepFrequency = 0.8
        clearExisting = False
        for i in range(len(footStepsList)):
            self.motion.setFootStepsWithSpeed(
                footStepsList[i][0],
                footStepsList[i][1],
                [stepFrequency],
                clearExisting)

    def sidestepL(self):
        footStepsList = []
        footStepsList.append([["LLeg"], [[0.00, 0.16, 0.0]]])
        footStepsList.append([["RLeg"], [[0.00, -0.1, 0.0]]])
        stepFrequency = 0.8
        clearExisting = False
        for i in range(len(footStepsList)):
            self.motion.setFootStepsWithSpeed(
                footStepsList[i][0],
                footStepsList[i][1],
                [stepFrequency],
                clearExisting)

    def insulte(self):
        L = ["Ma grand-mère joue mieux que toi",
             "Ba alors, casse toi pauvre con", "Allez Paris",
             "Vous n'avez pas honte?", "Ba alors, on attend pas Patrick?",
             "Je suis pas chasseur mais je lui mettrai bien une cartouche",
             "Poulet braisé mamène", "Benoit Zère rappeur du finistère",
             "Benoit Zère mon dieu", "Votez Troliste", "Send Nudes"]
        a = np.random.randint(0, len(L))
        self.tts.say(L[a])

    def shoot(self):
        # Set NAO in Stiffness On
        # StiffnessOn(proxy)

        # Send NAO to Pose Init
        self.postureProxy.goToPosture("StandInit", 0.5)

        # Activate Whole Body Balancer
        isEnabled = True
        self.motion.wbEnable(isEnabled)

        # Legs are constrained fixed
        stateName = "Fixed"
        supportLeg = "Legs"
        self.motion.wbFootState(stateName, supportLeg)

        # Constraint Balance Motion
        isEnable = True
        supportLeg = "Legs"
        self.motion.wbEnableBalanceConstraint(isEnable, supportLeg)

        # Com go to LLeg
        supportLeg = "LLeg"
        duration = 2.0
        self.motion.wbGoToBalance(supportLeg, duration)

        # RLeg is free
        stateName = "Free"
        supportLeg = "RLeg"
        self.motion.wbFootState(stateName, supportLeg)

        # RLeg is optimized
        effectorName = "RLeg"
        axisMask = 63
        space = self.motion.FRAME_ROBOT

        # Motion of the RLeg
        dx = 0.05                 # translation axis X (meters)
        dz = 0.05                 # translation axis Z (meters)
        dwy = 5.0*math.pi/180.0    # rotation axis Y (radian)

        times = [2.0, 2.7, 4.5]
        isAbsolute = False

        targetList = [
          [-dx, 0.0, dz, 0.0, +dwy, 0.0],
          [+dx, 0.0, dz, 0.0, 0.0, 0.0],
          [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

        self.motion.positionInterpolation(effectorName, space, targetList,
                                          axisMask, times, isAbsolute)

        # Example showing how to Enable Effector Control as an Optimization
        isActive = False
        self.motion.wbEnableEffectorOptimization(effectorName, isActive)

        # Com go to LLeg
        supportLeg = "RLeg"
        duration = 2.0
        self.motion.wbGoToBalance(supportLeg, duration)

        # RLeg is free
        stateName = "Free"
        supportLeg = "LLeg"
        self.motion.wbFootState(stateName, supportLeg)

        effectorName = "LLeg"
        self.motion.positionInterpolation(effectorName, space, targetList,
                                          axisMask, times, isAbsolute)

        time.sleep(1.0)

        # Deactivate Head tracking
        isEnabled = False
        self.motion.wbEnable(isEnabled)

        # send robot to Pose Init
        self.postureProxy.goToPosture("StandInit", 0.5)
