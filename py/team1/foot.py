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
              'forward', 'backward','shooting']

    transitions = [#état de départ idle
            {'trigger': 'sleep', 'source': 'idle', 'dest': 'idle',
                'before': 'doSleep'},
			{'trigger': 'quit', 'source': 'idle', 'dest': 'end',
                'before': 'doQuit'},
			{'trigger': 'standby', 'source': 'idle', 'dest': 'rest',
                'before': 'doStandby'}
            ]+#état de départ end,on ne peut pas sortir de l'état end
			
			[ {'trigger': 'quit', 'source': 'end', 'dest': 'end',
                'before': 'doQuit'}
			]+#état de départ leftward
			
			[ {'trigger': 'left', 'source': 'leftward', 'dest': 'leftward',
                'before': 'doLeft'},
			{'trigger': 'right', 'source': 'leftward', 'dest': 'rightward',
                'before': 'doRight'},
			{'trigger': 'standby', 'source': 'leftward', 'dest': 'rest',
                'before': 'doStandby'},
			{'trigger': 'go', 'source': 'leftward', 'dest': 'forward',
                'before': 'doGo'},
			{'trigger': 'goback', 'source': 'leftward', 'dest': 'backward',
                'before': 'doGoback'},
			{'trigger': 'shoot', 'source': 'leftward', 'dest': 'shooting',
                'before': 'doShoot'},
			{'trigger': 'sleep', 'source': 'leftward', 'dest': 'idle',
                'before': 'doSleep'},
			{'trigger': 'quit', 'source': 'leftward', 'dest': 'end',
                'before': 'doQuit'}
			]+#état de départ rightward
			
			[ {'trigger': 'right', 'source': 'rightward', 'dest': 'rightward',
                'before': 'doRight'},
			{'trigger': 'standby', 'source': 'rightward', 'dest': 'rest',
                'before': 'doStandby'},
			{'trigger': 'go', 'source': 'rightward', 'dest': 'forward',
                'before': 'doGo'},
			{'trigger': 'goback', 'source': 'rightward', 'dest': 'backward',
                'before': 'doGoback'},
			{'trigger': 'shoot', 'source': 'rightward', 'dest': 'shooting',
                'before': 'doShoot'},
			{'trigger': 'sleep', 'source': 'rightward', 'dest': 'idle',
                'before': 'doSleep'},
			{'trigger': 'quit', 'source': 'rightward', 'dest': 'end',
                'before': 'doQuit'},
			{'trigger': 'left', 'source': 'rightward', 'dest': 'leftward',
                'before': 'doLeft'}
			]+#état de départ rest
			
			[ {'trigger': 'standby', 'source': 'rest', 'dest': 'rest',
                'before': 'doStandby'},
			{'trigger': 'go', 'source': 'rest', 'dest': 'forward',
                'before': 'doGo'},
			{'trigger': 'goback', 'source': 'rest', 'dest': 'backward',
                'before': 'doGoback'},
			{'trigger': 'shoot', 'source': 'rest', 'dest': 'shooting',
                'before': 'doShoot'},
			{'trigger': 'sleep', 'source': 'rest', 'dest': 'idle',
                'before': 'doSleep'},
			{'trigger': 'quit', 'source': 'rest', 'dest': 'end',
                'before': 'doQuit'},
			{'trigger': 'left', 'source': 'rest', 'dest': 'leftward',
                'before': 'doLeft'},
			{'trigger': 'right', 'source': 'rest', 'dest': 'rightward',
                'before': 'doRight'}
			]+#état de départ forward
			
			[ {'trigger': 'go', 'source': 'forward', 'dest': 'forward',
                'before': 'doGo'},
			{'trigger': 'goback', 'source': 'forward', 'dest': 'backward',
                'before': 'doGoback'},
			{'trigger': 'shoot', 'source': 'forward', 'dest': 'shooting',
                'before': 'doShoot'},
			{'trigger': 'sleep', 'source': 'forward', 'dest': 'idle',
                'before': 'doSleep'},
			{'trigger': 'quit', 'source': 'forward', 'dest': 'end',
                'before': 'doQuit'},
			{'trigger': 'left', 'source': 'forward', 'dest': 'leftward',
                'before': 'doLeft'},
			{'trigger': 'right', 'source': 'forward', 'dest': 'rightward',
                'before': 'doRight'},
			{'trigger': 'standby', 'source': 'forward', 'dest': 'rest',
                'before': 'doStandby'}
			]+#état de départ backward
			
			[ {'trigger': 'goback', 'source': 'backward', 'dest': 'backward',
                'before': 'doGoback'},
			{'trigger': 'shoot', 'source': 'backward', 'dest': 'shooting',
                'before': 'doShoot'},
			{'trigger': 'sleep', 'source': 'backward', 'dest': 'idle',
                'before': 'doSleep'},
			{'trigger': 'quit', 'source': 'backward', 'dest': 'end',
                'before': 'doQuit'},
			{'trigger': 'left', 'source': 'backward', 'dest': 'leftward',
                'before': 'doLeft'},
			{'trigger': 'right', 'source': 'backward', 'dest': 'rightward',
                'before': 'doRight'},
			{'trigger': 'standby', 'source': 'backward', 'dest': 'rest',
                'before': 'doStandby'},
			{'trigger': 'go', 'source': 'backward', 'dest': 'forward',
                'before': 'doGo'}
			]+#état de départ shooting, après le tire le nao se remet droit 
			#et laisse la main au joueur
			
			[{'trigger': 'standby', 'source': 'shooting', 'dest': 'rest',
                'before': 'doStandby'}
			]
			

    machine = Machine(model=nao, states=states, transitions=transitions,
                      initial='idle', ignore_invalid_triggers=True)

    pg.init()
    window = pg.display.set_mode((640, 480))
    pg.draw.rect(window, (0,255,0), (20, 20, 600, 200), 0)
    pg.display.flip()

    pos = np.array([20, 20])
    naoRect = pg.draw.circle(window, (0,0,255), pos, 3) 

    run = True
    while run:
        for event in pg.event.get():
            if event.type == KEYDOWN:
                if event.key == K_b:
                    nao.back()

                elif event.key == K_c:
                    nao.rest()

                elif event.key == K_g:
                    nao.go()

                elif event.key == K_l:
                    nao.turn_leftward()

                elif event.key == K_r:
                    nao.turn_rightward()

                elif event.key == K_s:
                    nao.stop()

                elif event.key == K_w:
                    nao.wait()

        if nao.state == 'end':
            run = False
        if nao.state == 'forward': #à modifier
            nao.avoid_obstacle()
		#on peut remplacer cela par doQuit
        pos_prev = pos
        x, y, theta = nao.get_pos()
        pos = [x, y]
        naoRect.move_ip(pos-pos_prev)

        pg.display.flip()
        pg.time.delay(100)

    pg.quit()
    exit()


if __name__ == '__main__':
    main()
