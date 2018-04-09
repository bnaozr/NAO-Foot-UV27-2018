# -*- coding: utf-8 -*-
import argparse
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
    states = ['idle', 'end', 'turning_left', 'turning_right', 'rest',
              'walking', 'walking_back']

    transitions = [
            {'trigger': 'go', 'source': 'idle', 'dest': 'walking',
                'before': 'walk'},
            {'trigger': 'wait', 'source': 'walking', 'dest': 'idle',
                'before': 'stop_move'},
            {'trigger': 'turn_left', 'source': 'idle', 'dest': 'turning_left',
                'before': 'rotate_left'},
            {'trigger': 'wait', 'source': 'turning_left', 'dest': 'idle',
                'before': 'stop_move'},
            {'trigger': 'turn_right', 'source': 'idle',
                'dest': 'turning_right', 'before': 'rotate_right'},
            {'trigger': 'wait', 'source': 'turning_right', 'dest': 'idle',
                'before': 'stop_move'},
            {'trigger': 'back', 'source': 'idle', 'dest': 'walking_back',
                'before': 'walk_back'},
            {'trigger': 'wait', 'source': 'walking_back', 'dest': 'idle',
                'before': 'stop_move'},
            {'trigger': 'stop', 'source': 'rest', 'dest': 'end'},
            {'trigger': 'rest', 'source': 'idle', 'dest': 'rest',
                'before': 'crouch'},
            {'trigger': 'go', 'source': 'rest', 'dest': 'idle',
                'before': 'wake_up'}
            ]

    machine = Machine(model=nao, states=states, transitions=transitions,
                      initial='idle', ignore_invalid_triggers=True)

    pg.init()
    window = pg.display.set_mode((640, 480))

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
                    nao.turn_left()

                elif event.key == K_r:
                    nao.turn_right()

                elif event.key == K_s:
                    nao.stop()

                elif event.key == K_w:
                    nao.wait()

        if nao.state == 'end':
            run = False
        if nao.state == 'walking':
            nao.avoid_obstacle()
        time.sleep(0.1)


if __name__ == '__main__':
    main()
