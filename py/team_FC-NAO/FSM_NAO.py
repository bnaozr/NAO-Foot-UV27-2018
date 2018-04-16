import fsm
import time
import sys
import naocmd
import select 


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

f = fsm.fsm()
move_flag = False


def avance():
    global move_flag,lastevent
    if not(move_flag):
        move_flag=True
        naocmd.tout_droit(motion,posture,1)
        print "Avance d'un pas"  
    time.sleep(0.5)
    newKey,val = getKey(); 
    event="Again" # define the default event
    if newKey:
        if val=="l":
            move_flag=False
            event="Turn on the Left"  
        if val=="r":
            move_flag=False
            event="Turn on the Right"  
        if val=="w":
            move_flag=False
            event="Wait"
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
    newKey,val = getKey(); 
    event="Again" # define the default event
    if newKey:
        if val=="q":
            move_flag=False
            event="Walk"
        if val=="r":
            move_flag=False
            event="Turn on the Right"   
        if val=="w":
            move_flag=False
            event="Wait"
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
    newKey,val = getKey(); 
    event="Again" # define the default event
    if newKey:
        if val=="q":
            move_flag=False
            event="Walk"
        if val=="l":
            move_flag=False
            event="Turn on the Left"    
        if val=="w":
            move_flag=False
            event="Wait"
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
    newKey,val = getKey(); 
    event="Again" # define the default event
    if newKey:
        if val=="q":
            move_flag=False
            event="Walk"  
        if val=="s":
            move_flag=False
            event="End"
        if val=="l":
            move_flag=False
            event="Turn on the Left"  
        if val=="r":
            move_flag=False
            event="Turn on the Right"    
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
    f.add_state ("Evitement")

    f.add_event ("Walk")
    f.add_event ("Turn on the Right")
    f.add_event ("Turn on the Left")
    f.add_event ("End")
    f.add_event ("Wait")
    f.add_event ("Again")
    f.add_event ("Obstacle")


    f.add_transition ("Idle","Avance","Walk",avance)
    f.add_transition ("Avance","Avance","Again",avance)
    f.add_transition ("Avance","Evitement","Obstacle",evitement)
    f.add_transition ("Tourne a gauche","Evitement","Obstacle",evitement)
    f.add_transition ("Tourne a droite","Evitement","Obstacle",evitement)
    f.add_transition ("Evitement","Evitement","Again",evitement)
    f.add_transition ("Evitement","Avance","Walk",avance)
    f.add_transition ("Evitement","Idle","Wait",doWait)
    f.add_transition ("Evitement","Tourne a gauche","Turn on the Left",left)
    f.add_transition ("Evitement","Tourne a droite","Turn on the Right",right)
    f.add_transition ("Avance","Tourne a gauche","Turn on the Left",left)
    f.add_transition ("Tourne a gauche","Tourne a gauche","Again",left)
    f.add_transition ("Avance","Tourne a droite","Turn on the Right",right)
    f.add_transition ("Tourne a gauche","Avance","Walk",avance)
    f.add_transition ("Tourne a droite","Avance","Walk",avance)
    f.add_transition ("Tourne a droite","Tourne a gauche","Turn on the Left",left)
    f.add_transition ("Tourne a gauche","Tourne a droite","Turn on the Right",right)
    f.add_transition ("Tourne a droite","Tourne a droite","Again",right)
    f.add_transition ("Tourne a droite","Idle","Wait",doWait)
    f.add_transition ("Tourne a gauche","Idle","Wait",doWait)
    f.add_transition ("Idle","Mission terminee","End",end)
    f.add_transition ("Idle","Idle","Again",doWait)
    f.add_transition ("Avance","Idle","Wait",doWait)
    f.add_transition ("Idle","Tourne a gauche","Turn on the Left",left)
    f.add_transition ("Idle","Tourne a droite","Turn on the Right",right)

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



