import fsm
import time
import sys
import nao
from key import *
from nao import *
# use keyboard to control the fsm
#  w : event "Wait"
#  s : event "Stop"
#  g : event "Go" 

# global variables
f = fsm.fsm();  # finite state machine

if __name__== "__main__":
    
    # define the states
    f.add_state ("Idle")
    f.add_state ("Move")
    f.add_state ("Rotate")
    f.add_state ("End")
    f.add_state ("Avoid")
    # add here all the states you need
    # ...

    # defines the events 
    f.add_event ("Wait")
    f.add_event ("TurnL")
    f.add_event ("TurnR")
    f.add_event ("Go")
    f.add_event ("Stop")
    f.add_event ("Obstacle")
    f.add_event ("Nothing")
    # add here all the events you need
    # ...
   
    # defines the transition matrix
    # current state, next state, event, action in next state
    f.add_transition ("Idle","Idle","Wait",doWait)
    f.add_transition ("Idle","Rotate","TurnR",doTurnR)
    f.add_transition ("Idle","Rotate","TurnL",doTurnL)
    f.add_transition ("Idle","Move","Go",doMotion)
    f.add_transition ("Idle","End","Stop",doStopAll)
    f.add_transition ("Move","Idle","Wait",doWait)
    f.add_transition ("Move","Move","Go",doMotion)
    f.add_transition ("Move","Rotate","TurnL",doTurnL)
    f.add_transition ("Move","Rotate","TurnR",doTurnR)
    f.add_transition ("Move","End","Stop",doStopAll)
    f.add_transition ("Rotate","Idle","Wait",doWait)
    f.add_transition ("Rotate","Move","Go",doMotion)
    f.add_transition ("Rotate","Rotate","TurnL",doTurnL)
    f.add_transition ("Rotate","Rotate","TurnR",doTurnR)
    f.add_transition ("Rotate","End","Stop",doStopAll)
    
    f.add_transition ("Move","Avoid","Obstacle",doAvoid)
    f.add_transition ("Avoid","Avoid","Obstacle",doAvoid)
    f.add_transition ("Avoid","Move","Nothing",doMotion)
    f.add_transition ("Avoid","End","Stop",doStopAll)
    f.add_transition ("Avoid","Idle","Wait",doWait)
    f.add_transition ("Avoid","Rotate","TurnL",doTurnL)
    f.add_transition ("Avoid","Rotate","TurnR",doTurnR)
    
    
    
    # add here all the transitions you need
    # ...

    # initial state
    f.set_state ("Idle") # ... replace with your initial state
    # first event
    f.set_event ("Wait") # ...  replace with you first event 
    # end state
    end_state = "End" # ... replace  with your end state

 
    # fsm loop
    run = True   
    while (run):
        funct = f.run () # function to be executed in the new state
        if f.curState != end_state:
            newEvent = funct() # new event when state action is finished
            print "New Event : ",newEvent
            f.set_event(newEvent) # set new event for next transition
        else:
            funct()
            run = False
            
    print "End of the programm"



