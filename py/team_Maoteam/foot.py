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
              'forward', 'backward', 'shooting', 'shouting',
              'lateralShuffelLeftward', 'lateralShuffelRightward', 'joyMove']


    machine = Machine(model=nao, states=states, transitions=[],
                      initial='idle', ignore_invalid_triggers=True)
    
    # Ajout des états par états de destination
    
    # Destination idle
    sourceIdle = ['idle', 'leftward', 'rightward', 'rest', 'forward',
                  'backward', 'rest', 'joyMove', 
                  'lateralShuffelLeftward', 'lateralShuffelRightward']
    machine.add_transition(trigger='sleep', source=sourceIdle, dest='idle',
                           before='doSleep')
    # Destination end
    sourceEnd = ['idle', 'end', 'leftward', 'rightward','rest', 'forward',
                 'backward', 'joyMove', 'lateralShuffelLeftward',
                 'lateralShuffelRightward']
    machine.add_transition(trigger='quit', source=sourceEnd, dest='end', 
                           before='doQuit')
    # Destination 'leftward'
    sourceLeftward = ['leftward', 'rest', 'rightward', 'forward', 'backward',
            'lateralShuffelLeftward', 'lateralShuffelRightward', 'joyMove']
    machine.add_transition(trigger='left', source=sourceLeftward, dest='leftward',
                           before='doLeft')
    # Destination 'rightward'
    sourceRightward = ['leftward', 'rightward', 'rest', 'forward', 'backward',
            'lateralShuffelLeftward', 'lateralShuffelRightward', 'joyMove']
    machine.add_transition(trigger='right', source=sourceRightward, dest='rightward',
                           before='doRight')
    # Destination 'rest'
    sourceRest=['idle', 'leftward', 'rightward', 'rest', 'forward', 'backward',
               'shooting','shouting', 'lateralShuffelLeftward',
               'lateralShuffelRightward', 'joyMove']
    machine.add_transition(trigger='standby', source=sourceRest, dest='rest',
                           before='doStandby')
    # Destination 'forward'
    sourceForward = ['leftward', 'rightward', 'rest', 'forward', 'backward',
            'lateralShuffelLeftward', 'lateralShuffelRightward', 'joyMove']
    machine.add_transition(trigger='go', source=sourceForward, dest='forward',
                           before='doGo')
    # Destination backward
    sourceBackward = ['leftward', 'rightward', 'rest', 'forward', 'backward',
            'lateralShuffelLeftward', 'lateralShuffelRightward', 'joyMove']
    machine.add_transition(trigger='goback', source=sourceBackward, dest='backward',
                           before='doGoback')
    # Destination 'shooting'
    sourceShooting = ['leftward', 'rightward', 'rest', 'forward', 'backward',
            'lateralShuffelLeftward', 'lateralShuffelRightward', 'joyMove']
    machine.add_transition(trigger='shoot', source=sourceShooting, dest='shooting',
                           before='doShoot')
    # Destination 'shouting'
    sourceShouting = ['rest']
    machine.add_transition(trigger='shout', source=sourceShouting, dest='shouting',
                           before='doShout')
    # Destination 'lateralShuffelLeftward'
    sourceLateralShuffelLeftward = ['leftward', 'rightward', 'rest',
                                    'forward','backward',
                                    'lateralShuffelLeftward',
                                    'lateralShuffelRightward']
    machine.add_transition(trigger='lateralShuffelLeft',
                           source=sourceLateralShuffelLeftward,
                           dest='lateralShuffelLeftward',
                           before='doLateralShuffelLeft')
    # Destination 'lateralShuffelRightward'
    sourceLateralShuffelRightward = ['leftward', 'rightward', 'rest',
                                     'forward','backward',
                                     'lateralShuffelLeftward',
                                     'lateralShuffelRightward', 'joyMove']
    machine.add_transition(trigger='lateralShuffelRight',
                           source=sourceLateralShuffelRightward ,
                           dest='lateralShuffelRightward',
                           before='doLateralShuffelRight')

    # Destination 'joyMove'
    sourceJoystick = ['backward', 'foreward', 'joyMove',
                      'lateralShuffelLeftward', 'lateralShuffelRightward',
                      'leftward', 'rest', 'rightward']
    machine.add_transition(trigger='joystick', source=sourceJoystick, dest='joyMove',
                           before='doJoyMove')

    xref, yref, thetaRef = nao.get_pos()
    scale = 50
    window_width = 640
    window_height = 480
    pg.init()
    window = pg.display.set_mode((window_width, window_height))

    detect_obstacle = True

    pg.joystick.init()
    jTolerance = 0.2

    for i in range(pg.joystick.get_count()):
        pg.joystick.Joystick(i).init()

    run = True
    while run:
        for event in pg.event.get():
            if event.type == JOYAXISMOTION:
                if event.axis == 0:
                    if abs(event.value) < jTolerance:
                        nao.set_y_speed(0)
                    else:
                        nao.set_y_speed(-event.value)
                    nao.joystick()

                if event.axis == 1:
                    if abs(event.value) < jTolerance:
                        nao.set_x_speed(0)
                    else:
                        nao.set_x_speed(-event.value)
                    nao.joystick()

                if event.axis == 2:
                    if abs(event.value) < jTolerance:
                        nao.set_rotation_speed(0)
                    else:
                        nao.set_rotation_speed(-event.value)
                    nao.joystick()

            if event.type == JOYBUTTONDOWN:
                if event.button == 0:
                    nao.shoot()

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
                    detect_obstacle = not detect_obstacle

        if nao.state == 'end':
            run = False
        if nao.state == 'forward' and detect_obstacle:
            nao.avoid_obstacle()

        x, y, theta = nao.get_pos()
        x = int((x-xref)*scale)+window_width/2
        y = -int((y-yref)*scale)+window_height/2
        
        xb, yb, _, _ = nao.getPosBall(xref,yref,thetaRef)
        xb = int((xb)*scale)+l/2 
        yb = -int((yb)*scale)+h/2
        
        window.fill((0, 255, 0))
        pg.draw.circle(window, (0, 0, 255), (x, y), 6)
        pg.draw.circle(window, (255,255,0), (xb,yb), 3)
        
        pg.display.flip()
        pg.time.delay(100)

    pg.quit()
    exit()


if __name__ == '__main__':
    main()
