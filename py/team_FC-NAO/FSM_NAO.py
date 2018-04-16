#Deamon pour lire les touches ?
#Manette Play ? https://gist.github.com/claymcleod/028386b860b75e4f5472

import fsm
import time
import sys
import naocmd
import select 
import pygame as pg


Mouvement=1
x=1
y=0



#print("Nombre d'axes:", Notrejoystick.get_numaxes())
#print("Nombre de boutons :", Notrejoystick.get_numbuttons())
#print("Trackballs :", Notrejoystick.get_numballs())
#print("Hats :", Notrejoystick.get_numhats())
#print("Id du Joystick:", Notrejoystick.get_id())
#print("Nom du Joystick:", Notrejoystick.get_name())

def trouve_mouvement(a,b,c,t):
    global Mouvement
    if t==1:
        print("Feu Jean Mi'")
        Mouvement=1
        return()
    if (abs(c)<0.8 and Mouvement not in [10,11]):
        if b<-0.8 and abs(a)<0.8 and t!=1:
            print("Avance tout droit")
            Mouvement=2
            return()
        if b>0.8 and abs(a)<0.8 and t!=1:
            print("Recule tout droit")
            Mouvement=3
            return()
        if a>0.8 and abs(b)<0.8 and t!=1:
            print("Decale sur la droite")
            Mouvement=4
            return()
        if a<-0.8 and abs(b)<0.8 and t!=1:
            print("Decale sur la gauche") 
            Mouvement=5  
            return()
        if a>0.8 and b>0.8 and t!=1:
            print("Recule vers la droite") 
            Mouvement=6
            return()
        if a<-0.8 and b<-0.8 and t!=1:
            print("Avance vers la gauche")
            Mouvement=7
            return()
        if a>0.8 and b<-0.8 and t!=1:
            print("Avance vers la droite")
            Mouvement=8
            return()
        if a<-0.8 and b>0.8 and t!=1:
            print("Recule vers la gauche")
            Mouvement=9
            return()
    if (abs(a) and Mouvement not in [2,3,4,5,6,7,8,9]) or (abs(b) and Mouvement not in [2,3,4,5,6,7,8,9]):
        if c<-0.8 and t!=1:
            print("Tourne vers la gauche")
            Mouvement=10
            return()
        if c>0.8 and t!=1:
            print("Tourne vers la droite")
            Mouvement=11
            return()
    if t==0 and abs(c)<0.8 and abs(a)<0.8 and abs(b)<0.8:
        print("Finis ton mouvement")
        Mouvement=0
        return()

try:
    dist=float(sys.argv[3])
except:
    dist=0.6
    

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def getKey():
    #tty.setcbreak(sys.stdin.fileno())
    c='s'
    cok=False
    if isData():
        c = sys.stdin.read(1)
        cok=True
    return cok,c

def getJoystick():
    cok= False
    AX0=Notrejoystick.get_axis(0)
    AX1=Notrejoystick.get_axis(1)
    AX2=Notrejoystick.get_axis(2)
    print(AX0)
    print(AX1)
    print(AX2)
    Tir=Notrejoystick.get_button(0)
    print(Tir)
    trouve_mouvement(AX0,AX1,AX2,Tir)
    if Mouvement==0:
        val=t_wait
    if Mouvement==1:
        val=t_tir
    if Mouvement==2:
        val=t_avance
        y=0        
    if Mouvement==3:
        val=t_b
    if Mouvement==4:
        val=t_r
    if Mouvement==5:
        val=t_l
    if Mouvement==6:
        val=t_b
    if Mouvement==7:
        val= t_avance
        x=1
        y=-1
    if Mouvement==8:
        val= t_avance
        x=1
        y=1
    if Mouvement==9:
        val= t_b
    if Mouvement==10:
        val=t_pivot_l
    if Mouvement==11:
        val=t_pivot_r
    print(val)
    print(cok)
    return(cok,val)
    
global getMouv    
getMouv=getKey

try:
    joy=int(sys.argv[4])
    if joy:
        getMouv=getJoystick
        pg.init() # Initialise la video
        pg.joystick.init() # Initialise le joystick
        joysticks = [pg.joystick.Joystick(x) for x in range(pg.joystick.get_count())]
        Notrejoystick=pg.joystick.Joystick(0)
        Notrejoystick.init() # Initialise le joystick donne
        AX0=Notrejoystick.get_axis(0)
        AX1=Notrejoystick.get_axis(1)
        AX2=Notrejoystick.get_axis(2)
except: ()


f = fsm.fsm()
move_flag = False

#Touches:


fichier=open('doc_texte_touches','r')
touches=fichier.readlines()[0].split(',')
fichier.close()
t_avance=touches[0]
t_pivot_r=touches[5]
t_pivot_l=touches[4]
t_wait=touches[6]
t_r=touches[3]
t_l=touches[2]
t_b=touches[1]
t_end=touches[7][0]


def avance():
    global move_flag,lastevent
    if not(move_flag):
        move_flag=True
        naocmd.tout_droit(motion,posture,1,x,y)
        print"Avance d'un pas"
    time.sleep(0.5)
    
    newKey,val = getMouv();
    
    event="Again" # define the default event
    
    if newKey:
        if val==t_pivot_l:
            move_flag=False
            event="Turn on the Left"  
        if val==t_pivot_r:
            move_flag=False
            event="Turn on the Right"  
        if val==t_wait:
            move_flag=False
            event="Wait"
        if val==t_r:
            move_flag=False
            event="Right"
        if val==t_l:
            move_flag=False
            event="Left"
        if val==t_b:
            move_flag=False
            event="Go back"
    if naocmd.donnee_sonar(sonar,memory,motion,float(dist))[0]:
        move_flag=False
        event="Obstacle"
        lastevent="Walk"
    return event # return event to be able to define the transition

def left():
    global move_flag,lastevent
    if not(move_flag):
        move_flag=True
        naocmd.tourner_a_gauche(motion,1)
        print "Tourne a gauche"   
    time.sleep(0.5)
    newKey,val = getMouv(); 
    event="Again" # define the default event
    if newKey:
        if val==t_avance:
            move_flag=False
            event="Walk"
        if val==t_pivot_r:
            move_flag=False
            event="Turn on the Right"   
        if val==t_wait:
            move_flag=False
            event="Wait"
        if val==t_r:
            move_flag=False
            event="Right"
        if val==t_l:
            move_flag=False
            event="Left"
        if val==t_b:
            move_flag=False
            event="Go back"
    if naocmd.donnee_sonar(sonar,memory,motion,float(dist))[0]:
        move_flag=False
        event="Obstacle"
        lastevent="Turn on the Left"  
    return event # return event to be able to define the transition

def right():
    global move_flag,lastevent
    if not(move_flag):
        move_flag=True
        naocmd.tourner_a_droite(motion,1)    
        print "Tourne a droite"   
    time.sleep(0.5)
    newKey,val = getMouv(); 
    event="Again" # define the default event
    if newKey:
        if val==t_avance:
            move_flag=False
            event="Walk"
        if val==t_pivot_l:
            move_flag=False
            event="Turn on the Left"    
        if val==t_wait:
            move_flag=False
            event="Wait"
        if val==t_r:
            move_flag=False
            event="Right"
        if val==t_l:
            move_flag=False
            event="Left"
        if val==t_b:
            move_flag=False
            event="Go back"
    if naocmd.donnee_sonar(sonar,memory,motion,float(dist))[0]:
        move_flag=False
        event="Obstacle"
    lastevent="Turn on the Right"   
    return event # return event to be able to define the transition

def doWait():
    global move_flag
    if not(move_flag):
        move_flag=True
        naocmd.stop(motion)
        print "En Pause"   
    time.sleep(0.5)
    newKey,val = getMouv(); 
    event="Again" # define the default event
    if newKey:
        if val==t_avance:
            move_flag=False
            event="Walk"  
        if val==t_end:
            move_flag=False
            event="End"
        if val==t_pivot_l:
            move_flag=False
            event="Turn on the Left"  
        if val==t_pivot_r:
            move_flag=False
            event="Turn on the Right"
        if val==t_r:
            move_flag=False
            event="Right"
        if val==t_l:
            move_flag=False
            event="Left"
        if val==t_b:
            move_flag=False
            event="Go back"    
    return event # return event to be able to define the transition

def evitement():
    global move_flag
    if not(move_flag):
        move_flag=True
        #Si cote gauche detecte en premier alors on tourne a droite 
        if naocmd.donnee_sonar(sonar,memory,motion,float(dist))[1] < naocmd.donnee_sonar(sonar,memory,motion,float(dist))[2]:
            naocmd.tourner_a_droite(motion,1)
        else:
            naocmd.tourner_a_gauche(motion,1)
        print "Detection Obstacle"
    time.sleep(0.5)
    if not(naocmd.donnee_sonar(sonar,memory,motion,0.1+float(dist))[0]):
        print "Fin d'evitement"
        move_flag=False
        return lastevent
    else:
        return "Again"   

def goRight():
    global move_flag,lastevent
    if not(move_flag):
        move_flag=True
        naocmd.decal_droite(motion,posture,1)    
        print "A droite"   
    time.sleep(0.5)
    newKey,val = getMouv(); 
    event="Again" # define the default event
    if newKey:
        if val==t_avance:
            move_flag=False
            event="Walk"
        if val==t_pivot_l:
            move_flag=False
            event="Turn on the Left"
        if val==t_pivot_r:
            move_flag=False
            event="Turn on the Right"       
        if val==t_wait:
            move_flag=False
            event="Wait"
        if val==t_l:
            move_flag=False
            event="Left"
        if val==t_b:
            move_flag=False
            event="Go back"
    if naocmd.donnee_sonar(sonar,memory,motion,float(dist))[0]:
        move_flag=False
        event="Obstacle"
    lastevent="Right"   
    return event # return event to be able to define the transition

def goLeft():
    global move_flag,lastevent
    if not(move_flag):
        move_flag=True
        naocmd.decal_gauche(motion,posture,1)    
        print "A gauche"   
    time.sleep(0.5)
    newKey,val = getMouv(); 
    event="Again" # define the default event
    if newKey:
        if val==t_avance:
            move_flag=False
            event="Walk"
        if val==t_pivot_l:
            move_flag=False
            event="Turn on the Left"
        if val==t_pivot_r:
            move_flag=False
            event="Turn on the Right"       
        if val==t_wait:
            move_flag=False
            event="Wait"
        if val==t_r:
            move_flag=False
            event="Right"
        if val==t_b:
            move_flag=False
            event="Go back"
    if naocmd.donnee_sonar(sonar,memory,motion,float(dist))[0]:
        move_flag=False
        event="Obstacle"
    lastevent="Left"   
    return event # return event to be able to define the transition

def goBack():
    global move_flag,lastevent
    if not(move_flag):
        move_flag=True
        naocmd.marche_arriere(motion,posture,1)    
        print "Recule"   
    time.sleep(0.5)
    newKey,val = getMouv(); 
    event="Again" # define the default event
    if newKey:
        if val==t_avance:
            move_flag=False
            event="Walk"
        if val==t_pivot_l:
            move_flag=False
            event="Turn on the Left"
        if val==t_pivot_r:
            move_flag=False
            event="Turn on the Right"       
        if val==t_wait:
            move_flag=False
            event="Wait"
        if val==t_r:
            move_flag=False
            event="Right"
        if val==t_l:
            move_flag=False
            event="Left"
    if naocmd.donnee_sonar(sonar,memory,motion,float(dist))[0]:
        move_flag=False
        event="Obstacle"
    lastevent="Go back"   
    return event # return event to be able to define the transition

    

def end():
    naocmd.fin(motion,posture)
    print "Mission terminee"


if __name__== "__main__":

    motion,posture,sonar,memory=naocmd.initialisation()
    

    f.add_state ("Idle") 
    f.add_state ("Avance")
    f.add_state ("Tourne a gauche")
    f.add_state ("Tourne a droite")
    f.add_state ("Misson terminee")
    f.add_state ("Droite")
    f.add_state ("Gauche")
    f.add_state ("Arriere")
    f.add_state ("Evitement")

    f.add_event ("Walk")
    f.add_event ("Turn on the Right")
    f.add_event ("Turn on the Left")
    f.add_event ("Right")
    f.add_event ("Left")
    f.add_event ("Go back")
    f.add_event ("End")
    f.add_event ("Wait")
    f.add_event ("Again")
    f.add_event ("Obstacle")



    f.add_transition ("Droite","Avance","Walk",avance)
    f.add_transition ("Droite","Droite","Again",goRight)
    f.add_transition ("Droite","Tourne a gauche","Turn on the Left",left)
    f.add_transition ("Droite","Tourne a droite","Turn on the Right",right)
    f.add_transition ("Droite","Gauche","Left",goLeft)
    f.add_transition ("Droite","Idle","Wait",doWait)
    f.add_transition ("Droite","Evitement","Obstacle",evitement)
    f.add_transition ("Droite","Arriere","Go back",goBack)

    f.add_transition ("Gauche","Avance","Walk",avance)
    f.add_transition ("Gauche","Gauche","Again",goLeft)
    f.add_transition ("Gauche","Tourne a gauche","Turn on the Left",left)
    f.add_transition ("Gauche","Tourne a droite","Turn on the Right",right)
    f.add_transition ("Gauche","Idle","Wait",doWait)
    f.add_transition ("Gauche","Droite","Right",goRight)
    f.add_transition ("Gauche","Evitement","Obstacle",evitement)
    f.add_transition ("Gauche","Arriere","Go back",goBack)

    f.add_transition ("Arriere","Avance","Walk",avance)
    f.add_transition ("Arriere","Arriere","Again",goBack)
    f.add_transition ("Arriere","Tourne a gauche","Turn on the Left",left)
    f.add_transition ("Arriere","Tourne a droite","Turn on the Right",right)
    f.add_transition ("Arriere","Idle","Wait",doWait)
    f.add_transition ("Arriere","Droite","Right",goRight)
    f.add_transition ("Arriere","Gauche","Left",goLeft)
    f.add_transition ("Arriere","Evitement","Obstacle",evitement)
    
    f.add_transition ("Avance","Droite","Right",goRight)
    f.add_transition ("Avance","Gauche","Left",goLeft)
    f.add_transition ("Avance","Arriere","Go back",goBack)
    f.add_transition ("Avance","Avance","Again",avance)
    f.add_transition ("Avance","Evitement","Obstacle",evitement)
    f.add_transition ("Avance","Tourne a gauche","Turn on the Left",left)
    f.add_transition ("Avance","Tourne a droite","Turn on the Right",right)
    f.add_transition ("Avance","Idle","Wait",doWait)

    f.add_transition ("Idle","Avance","Walk",avance)
    f.add_transition ("Idle","Mission terminee","End",end)
    f.add_transition ("Idle","Idle","Again",doWait)
    f.add_transition ("Idle","Tourne a gauche","Turn on the Left",left)
    f.add_transition ("Idle","Tourne a droite","Turn on the Right",right)
    f.add_transition ("Idle","Droite","Right",goRight)
    f.add_transition ("Idle","Gauche","Left",goLeft)
    f.add_transition ("Idle","Arriere","Go back",goBack)

    f.add_transition ("Tourne a gauche","Evitement","Obstacle",evitement)
    f.add_transition ("Tourne a gauche","Tourne a gauche","Again",left)
    f.add_transition ("Tourne a gauche","Avance","Walk",avance)
    f.add_transition ("Tourne a gauche","Tourne a droite","Turn on the Right",right)
    f.add_transition ("Tourne a gauche","Idle","Wait",doWait)
    f.add_transition ("Tourne a gauche","Droite","Right",goRight)
    f.add_transition ("Tourne a gauche","Gauche","Left",goLeft)
    f.add_transition ("Tourne a gauche","Arriere","Go back",goBack)

    f.add_transition ("Tourne a droite","Avance","Walk",avance)
    f.add_transition ("Tourne a droite","Tourne a gauche","Turn on the Left",left)
    f.add_transition ("Tourne a droite","Evitement","Obstacle",evitement)
    f.add_transition ("Tourne a droite","Tourne a droite","Again",right)
    f.add_transition ("Tourne a droite","Idle","Wait",doWait)
    f.add_transition ("Tourne a droite","Droite","Right",goRight)
    f.add_transition ("Tourne a droite","Gauche","Left",goLeft)
    f.add_transition ("Tourne a droite","Arriere","Go back",goBack)

    f.add_transition ("Evitement","Evitement","Again",evitement)
    f.add_transition ("Evitement","Avance","Walk",avance)
    f.add_transition ("Evitement","Gauche","Left",goLeft)
    f.add_transition ("Evitement","Droite","Right",goRight)
    f.add_transition ("Evitement","Idle","Wait",doWait)
    f.add_transition ("Evitement","Tourne a gauche","Turn on the Left",left)
    f.add_transition ("Evitement","Tourne a droite","Turn on the Right",right)
    f.add_transition ("Evitement","Arriere","Go back",goBack)








    # initial state
    f.set_state ("Idle") 
    f.set_event ("Again")
    end_state="Mission terminee"
 
    # fsm loop
    run = True
    print "En marche"   
    while (run):
        funct = f.run () # function to be executed in the new state
        if f.curState != end_state:
            newEvent = funct()
            #print "New Event : ",newEvent
            f.set_event(newEvent) # set new event for next transition
        else:
            funct()
            run = False
            
    print "End of the programm"



