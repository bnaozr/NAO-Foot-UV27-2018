#Deamon pour lire les touches ?
#Manette Play ? https://gist.github.com/claymcleod/028386b860b75e4f5472

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

#Touches:
t_avance="q"
t_pivot_r="r"
t_pivot_l="l"
t_wait="w"
t_r="d"
t_l="a"
t_b="b"
t_end="s"


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
    newKey,val = getKey(); 
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
    newKey,val = getKey(); 
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
    newKey,val = getKey(); 
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
    newKey,val = getKey(); 
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
    newKey,val = getKey(); 
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
        naocmd.decal_gauche(motion,posture,1)    
        print "Recule"   
    time.sleep(0.5)
    newKey,val = getKey(); 
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
    f.add_transition ("Droite","Droite","Right",goRight)
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



