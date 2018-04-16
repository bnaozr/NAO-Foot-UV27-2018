# -*- coding: utf-8 -*-
from naoqi import ALProxy
import numpy as np

class Nao:
    def __init__(self, ip, port):
        self.motion = ALProxy('ALMotion', ip, int(port))
        self.sonar = ALProxy('ALSonar', ip, int(port))
        self.memory = ALProxy('ALMemory', ip, int(port))
        self.posture = ALProxy("ALRobotPosture", ip, int(port))

        self.sonar.subscribe('nao')

        self.motion.wakeUp()
        
        self.ip=ip
        self.port=port

    def avoid_obstacle(self):
        d_left = self.memory.getData(
                "Device/SubDeviceList/US/Left/Sensor/Value")
        d_right = self.memory.getData(
                "Device/SubDeviceList/US/Right/Sensor/Value")

        if d_left < 0.3 or d_right < 0.3:
            self.standby()
            
            
    def rotateHead(self):
        self.motion.moveInit()
        self.motion.wbEnable(True)
        effectorName = "Head"
        self.motion.wbEnableEffectorControl(effectorName, True)
        h=self.get_pos()[2]
        xB, yB, xC, yC = self.getPosBall()
        if xB!=None and yB!=None and xC!=None and yC!=None:
            targetCoordinate = [0.0, np.arccos(h/xB)-np.arccos(h/xC), np.arctan(xB/yB)]
            self.motion.wbSetEffectorControl(effectorName, targetCoordinate)
        self.motion.wbEnable(False)

    def get_pos(self):
        return self.motion.getRobotPosition(True)
    
    def getPosBall(self):
        b, xLoc, yLoc, dballepx=self.detectBallon(self.ip, self.port)
        xb,yb,xc,yc=None,None,None,None
        if b:
            taille_px=1.9*10**-6
            dballe=dballepx*taille_px
            dballereel= 0.08  # diamètre de la balle en m
            g=dballereel/dballe
            f=556*taille_px # distance focale en m
            distance_balle=f*(1-g)
            xrob=self.get_pos()[0]
            yrob=self.get_pos()[1]
            Rz=self.get_pos()[5]
             
            coord_centre=[1280/2,yLoc]
            coord_balle=[xLoc,yLoc]
            
            #coordonnées de la balle dans le repère du robot(FrameRobot) en m
            y=-(coord_balle[0]-coord_centre[0])*taille_px
            x=np.sqrt(distance_balle**2-y**2)
            
            #coordonnées de la balle dans le repère frameworld en m
            xb=(x-xrob)*np.cos(Rz)-(y-yrob)*np.sin(Rz)
            yb=(y-yrob)*np.cos(Rz)+(x-xrob)*np.sin(Rz)
        
            #coordonnées du centre de l'image dans le repère frameworld en m
            xc=(distance_balle-xrob)*np.cos(Rz)-(-yrob)*np.sin(Rz)
            yc=(-yrob)*np.cos(Rz)+(distance_balle-xrob)*np.sin(Rz)
    
        return xb,yb,xc,yc
	
	  #fonction de transitions en doNomévénement
      
    def standUp(self):
        pNames = "Body"
        pStiffnessLists = 1.0
        pTimeLists = 1.0
        self.motion.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
        self.posture.goToPosture("LyingBelly", 0.5)
        self.posture.goToPosture("SitRelax", 0.5)
        self.posture.goToPosture("Sit", 0.5)
        self.posture.goToPosture("StandInit", 0.5)

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
	
	
