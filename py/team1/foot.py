# -*- coding: utf-8 -*-
import argparse
import numpy as np
import pygame as pg
import time

from pygame.locals import *
from transitions import Machine

from nao import Nao


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', help='addresse ip du nao')
    parser.add_argument('--port', help='port du nao', type=int)

    args = parser.parse_args()

    nao = Nao(args.ip, args.port)

    # FSM
    states = ['idle', 'end', 'leftward', 'rightward', 'rest',
              'forward', 'backward','shooting','shouting',
              'lateralShuffelLeftward','lateralShuffelRightward']
#
#    transitions = [#état de départ idle
#            {'trigger': 'sleep', 'source': 'idle', 'dest': 'idle',
#                'before': 'doSleep'},
#			{'trigger': 'quit', 'source': 'idle', 'dest': 'end',
#                'before': 'doQuit'},
#			{'trigger': 'standby', 'source': 'idle', 'dest': 'rest',
#                'before': 'doWakeUp'},
#
#      #état de départ end,on ne peut pas sortir de l'état end
#			{'trigger': 'quit', 'source': 'end', 'dest': 'end',
#                'before': 'doQuit'}, 
#
#      #état de départ leftward	
#			{'trigger': 'left', 'source': 'leftward', 'dest': 'leftward',
#                'before': 'doLeft'},
#			{'trigger': 'right', 'source': 'leftward', 'dest': 'rightward',
#                'before': 'doRight'},
#			{'trigger': 'standby', 'source': 'leftward', 'dest': 'rest',
#                'before': 'doStandby'},
#			{'trigger': 'go', 'source': 'leftward', 'dest': 'forward',
#                'before': 'doGo'},
#			{'trigger': 'goback', 'source': 'leftward', 'dest': 'backward',
#                'before': 'doGoback'},
#			{'trigger': 'shoot', 'source': 'leftward', 'dest': 'shooting',
#                'before': 'doShoot'},
#			{'trigger': 'sleep', 'source': 'leftward', 'dest': 'idle',
#                'before': 'doSleep'},
#			{'trigger': 'quit', 'source': 'leftward', 'dest': 'end',
#                'before': 'doQuit'},
#      
#      #état de départ rightward			
#			{'trigger': 'right', 'source': 'rightward', 'dest': 'rightward',
#                'before': 'doRight'},
#			{'trigger': 'standby', 'source': 'rightward', 'dest': 'rest',
#                'before': 'doStandby'},
#			{'trigger': 'go', 'source': 'rightward', 'dest': 'forward',
#                'before': 'doGo'},
#			{'trigger': 'goback', 'source': 'rightward', 'dest': 'backward',
#                'before': 'doGoback'},
#			{'trigger': 'shoot', 'source': 'rightward', 'dest': 'shooting',
#                'before': 'doShoot'},
#			{'trigger': 'sleep', 'source': 'rightward', 'dest': 'idle',
#                'before': 'doSleep'},
#			{'trigger': 'quit', 'source': 'rightward', 'dest': 'end',
#                'before': 'doQuit'},
#			{'trigger': 'left', 'source': 'rightward', 'dest': 'leftward',
#                'before': 'doLeft'},
#
#      #état de départ rest			
#			{'trigger': 'standby', 'source': 'rest', 'dest': 'rest',
#                'before': 'doStandby'},
#			{'trigger': 'go', 'source': 'rest', 'dest': 'forward',
#                'before': 'doGo'},
#			{'trigger': 'goback', 'source': 'rest', 'dest': 'backward',
#                'before': 'doGoback'},
#			{'trigger': 'shoot', 'source': 'rest', 'dest': 'shooting',
#                'before': 'doShoot'},
#			{'trigger': 'sleep', 'source': 'rest', 'dest': 'idle',
#                'before': 'doSleep'},
#			{'trigger': 'quit', 'source': 'rest', 'dest': 'end',
#                'before': 'doQuit'},
#			{'trigger': 'left', 'source': 'rest', 'dest': 'leftward',
#                'before': 'doLeft'},
#			{'trigger': 'right', 'source': 'rest', 'dest': 'rightward',
#                'before': 'doRight'},
#
#      #état de départ forward			
#			{'trigger': 'go', 'source': 'forward', 'dest': 'forward',
#                'before': 'doGo'},
#			{'trigger': 'goback', 'source': 'forward', 'dest': 'backward',
#                'before': 'doGoback'},
#			{'trigger': 'shoot', 'source': 'forward', 'dest': 'shooting',
#                'before': 'doShoot'},
#			{'trigger': 'sleep', 'source': 'forward', 'dest': 'idle',
#                'before': 'doSleep'},
#			{'trigger': 'quit', 'source': 'forward', 'dest': 'end',
#                'before': 'doQuit'},
#			{'trigger': 'left', 'source': 'forward', 'dest': 'leftward',
#                'before': 'doLeft'},
#			{'trigger': 'right', 'source': 'forward', 'dest': 'rightward',
#                'before': 'doRight'},
#			{'trigger': 'standby', 'source': 'forward', 'dest': 'rest',
#                'before': 'doStandby'},
#
#      #état de départ backward
#			{'trigger': 'goback', 'source': 'backward', 'dest': 'backward',
#                'before': 'doGoback'},
#			{'trigger': 'shoot', 'source': 'backward', 'dest': 'shooting',
#                'before': 'doShoot'},
#			{'trigger': 'sleep', 'source': 'backward', 'dest': 'idle',
#                'before': 'doSleep'},
#			{'trigger': 'quit', 'source': 'backward', 'dest': 'end',
#                'before': 'doQuit'},
#			{'trigger': 'left', 'source': 'backward', 'dest': 'leftward',
#                'before': 'doLeft'},
#			{'trigger': 'right', 'source': 'backward', 'dest': 'rightward',
#                'before': 'doRight'},
#			{'trigger': 'standby', 'source': 'backward', 'dest': 'rest',
#                'before': 'doStandby'},
#			{'trigger': 'go', 'source': 'backward', 'dest': 'forward',
#                'before': 'doGo'},
#
#      #état de départ shooting, après le tire le nao se remet droit 
#			#et laisse la main au joueur
#            {'trigger': 'standby', 'source': 'shooting', 'dest': 'rest',
#                'before': 'doStandby'},
#          #gestion de l'état: shouting, on ne peut crier que si le nao est à l'arrêt
#          {'trigger': 'standby', 'source': 'shooting', 'dest': 'rest',
#                'before': 'doStandby'},
#           {'trigger': 'standby', 'source': 'shooting', 'dest': 'rest',
#                'before': 'doStandby'}
#          
#          
#          
#          
#          
#          ]
			

    machine = Machine(model=nao, states=states, transitions=[],
                      initial='idle', ignore_invalid_triggers=True)
    
    # Ajout des états par états de destination
    
    # Destination idle
    sourceIdle = ['idle', 'leftward', 'rightward', 'rest', 'forward',
                  'backward', 'rest',
                  'lateralShuffelLeftward', 'lateralShuffelRightward']
    machine.add_transition(trigger='sleep', sourceIdle, dest='idle',
                           before='doSleep')
    # Destination end
    sourceEnd = ['idle', 'end', 'leftward', 'rightward','rest', 'forward', 'backward',
               'lateralShuffelLeftward', 'lateralShuffelRightward']
    machine.add_transition(trigger='quit', sourceEnd, dest='end', 
                           before='doQuit')
    # Destination 'leftward'
    sourceLeftward = ['leftward', 'rest', 'rightward', 'forward', 'backward',
            'lateralShuffelLeftward', 'lateralShuffelRightward']
    machine.add_transition(trigger='left', sourceLeftward, dest='leftward',
                           before='doLeft')
    # Destination 'rightward'
    sourceRightward = ['leftward', 'rightward', 'rest', 'forward', 'backward',
            'lateralShuffelLeftward', 'lateralShuffelRightward']
    machine.add_transition(trigger='right', sourceRightward, dest='rightward',
                           before='doRight')
    # Destination 'rest'
    sourceRest=['idle', 'leftward', 'rightward', 'rest', 'forward', 'backward',
               'shooting','shouting', 'lateralShuffelLeftward',
               'lateralShuffelRightward']
    machine.add_transition(trigger='standby', sourceRest, dest='rest',
                           before='doStandby')
    # Destination 'forward'
    sourceForward = ['leftward', 'rightward', 'rest', 'forward', 'backward',
            'lateralShuffelLeftward', 'lateralShuffelRightward']
    machine.add_transition(trigger='go', sourceForward, dest='forward',
                           before='doGo')
    # Destination backward
    sourceBackward = ['leftward', 'rightward', 'rest', 'forward', 'backward',
            'lateralShuffelLeftward', 'lateralShuffelRightward']
    machine.add_transition(trigger='goback', sourceBackward, dest='backward',
                           before='doGoback')
    # Destination 'shooting'
    sourceShooting = ['leftward', 'rightward', 'rest', 'forward', 'backward',
            'lateralShuffelLeftward', 'lateralShuffelRightward']
    machine.add_transition(trigger='shoot',  sourceShooting, dest='shooting',
                           before='doShoot')
    # Destination 'shouting'
    sourceShouting = ['rest']
    machine.add_transition(trigger='shout',  sourceShouting, dest='shouting',
                           before='doShout')
    # Destination 'lateralShuffelLeftward'
    sourceLateralShuffelLeftward = ['leftward', 'rightward', 'rest',
                                    'forward','backward',
                                    'lateralShuffelLeftward',
                                    'lateralShuffelRightward']
    machine.add_transition(trigger='lateralShuffelLeft',
                           sourceLateralShuffelLeftward,
                           dest='lateralShuffelLeftward',
                           before='doLateralShuffelLeft')
    # Destination 'lateralShuffelRightward'
    sourceLateralShuffelRightward = ['leftward', 'rightward', 'rest',
                                     'forward','backward',
                                     'lateralShuffelLeftward',
                                     'lateralShuffelRightward']
    machine.add_transition(trigger='lateralShuffelRight',
                           sourceLateralShuffelRightward ,
                           dest='lateralShuffelRightward',
                           before='doLateralShuffelRight')
    
    # IHM
    xref, yref, _ = nao.get_pos()
    scale = 50
    l = 640
    h = 480
    pg.init()
    window = pg.display.set_mode((l, h))

    detect_obstacle = True

    run = True
    while run:
        for event in pg.event.get():
            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    nao.goback()

                elif event.key == K_UP:
                    nao.go()

                elif event.key == K_LEFT:
                    nao.left()

                elif event.key == K_RIGHT:
                    nao.right()

                elif event.key == K_SPACE:
                    nao.shoot()

                elif event.key == K_q:
                    nao.quit()

                elif event.key == K_RETURN:
                    nao.standby()

                elif event.key == K_s:
                    nao.sleep()

                elif event.key == K_o:
                    detect_obstacle = !detect_obstacle

        if nao.state == 'end':
            run = False
        if nao.state == 'forward' and detect_obstacle:
            nao.avoid_obstacle()

        x, y, theta = nao.get_pos()
        x = int((x-xref)*scale)+l/2 
        y = -int((y-yref)*scale)+h/2
        window.fill((0,255,0))
        pg.draw.circle(window, (0,0,255), (x,y), 6)

        pg.display.flip()
        pg.time.delay(100)

    pg.quit()
    exit()


if __name__ == '__main__':
    main()
