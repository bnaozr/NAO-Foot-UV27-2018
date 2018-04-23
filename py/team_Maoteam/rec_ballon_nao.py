# -*- coding: utf8 -*-
import sys
import cv2
import numpy as np
from PIL import Image
from naoqi import ALProxy

def findOrangeFloats (imageWidth, imageHeight, cvImg, debug, color="Yellow"):
   found = False
   xSize, ySize = 0, 0
   xLoc, yLoc = 0, 0
   cvImgHSV = cv2.cvtColor(cvImg, cv2.COLOR_BGR2HSV) # convertit l'image avec l'encodage hsv
   if (debug): 
       cv2.imwrite('naoimg_hsv.png', cvImgHSV) # enregistre l'image avec l'encodage hsv
       
   ## Définit les paramètres hsv en fonction de la couleur choisie

   if color == "Orange":
      HSVMin= np.array([0,150,100]) 
      HSVMax= np.array([20,255,255])
   elif color == "Yellow":
      HSVMin= np.array([20,150,100]) 
      HSVMax= np.array([40,255,255])
   else:
      HSVMin= np.array([0,0,0]) 
      HSVMax= np.array([180,255,255])
      
   cvImgSegm0 = cv2.inRange(cvImgHSV, HSVMin, HSVMax) # applique un masque sur l'image pour uniquement recupérer les objets dans la couleur color
   

   cvImgSegm=cvImgSegm0 
   if (debug):
       cv2.imwrite('naoimg_thr.png', cvImgSegm)

   (ctrs,_) = cv2.findContours(cvImgSegm.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # récupère les contours

   ## Cherche le plus gros objet de couleur color
   
   cvCtr = np.zeros((imageHeight,imageWidth,3), np.uint8)
   cvMax = np.zeros((imageHeight,imageWidth,1), np.uint8)
   maxAreaOn = 0
   
   for ctrs1 in ctrs:
      areaOn = cv2.contourArea(ctrs1)
      if (areaOn > maxAreaOn):
         maxAreaOn = areaOn
         bestCtrs = ctrs1
      if (debug):
         cv2.drawContours(cvCtr, [ctrs1], 0, (0,255,0), 1)

   if (debug):
      cv2.imwrite('naoimg_ctr.png', cvCtr)


   ## On considère cet objet s'il a une taille supérieure à 30 pixels
   
   if maxAreaOn >= 30:
      cvMax[:,:,:]=0
      cv2.drawContours(cvMax, [bestCtrs], 0,  (255), 1)
      if (debug):
          cv2.imwrite('naoimg_max.png', cvMax)
      areaOn = cv2.countNonZero(cvMax)

      
      MM = cv2.moments(bestCtrs)
      bRect = cv2.boundingRect(bestCtrs)

      found = True
      xLoc = int(MM['m10'] / MM['m00']);yLoc = int(MM['m01'] / MM['m00'])
      xSize = bRect[2]
      ySize = bRect[3]
      
   return found,xLoc,yLoc, max(xSize, ySize)


def detectBallon(IP, PORT):
  camProxy = ALProxy("ALVideoDevice", IP, PORT)
  resolution = 1    
  colorSpace = 11   
  camNum = 0 
  fps = 1; 
  camProxy.setParam(18, camNum)
  try:
     videoClient = camProxy.subscribe("python_client", 
                                         resolution, colorSpace, fps)
  except:
    camProxy.unsubscribe("python_client")
    videoClient = camProxy.subscribe("python_client", 
                                       resolution, colorSpace, fps)

  naoImage = camProxy.getImageRemote(videoClient)
  camProxy.unsubscribe(videoClient)
  imageWidth = naoImage[0]
  imageHeight = naoImage[1]
  array = naoImage[6]
  pilImg = Image.frombytes("RGB", (imageWidth, imageHeight), array)
  cvImg = np.array(pilImg)
  cvImg = cvImg[:, :, ::-1].copy() 
  return findOrangeFloats(imageWidth, imageHeight, cvImg, True, color="Yellow")
  


if __name__ == '__main__':
    
  IP = "localhost"  # Replace here with your NaoQi's IP address.
  PORT = 9559

  # Read IP address from first argument if any.
  if len(sys.argv) > 1:
    IP = sys.argv[1]

  naoImage = detectBallon(IP, PORT)