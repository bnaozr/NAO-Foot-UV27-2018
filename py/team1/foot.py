# -*- coding: utf-8 -*-
import curses
import logging
import time

from transitions import Machine

from nao import Nao


def main(stdscr):
    curses.echo()
    stdscr.addstr(0, 0, 'IP: ')
    ip = stdscr.getstr(0, 5)
    stdscr.addstr(1, 0, 'port: ')
    port = stdscr.getstr(1, 6)

    curses.noecho()
    stdscr.clear()
    stdscr.nodelay(True)
    stdscr.scrollok(True)

    nao = Nao(ip, port)

    # Logging
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt='%(message)s\r'))
    logging.getLogger('transitions').addHandler(handler)

    # FSM
    states = ['idle', 'end', 'turning_left', 'turning_right', 'rest', 'walking', 'walking_back']

    transitions = [
            {'trigger': 'go', 'source': 'idle', 'dest': 'walking', 'before': 'walk'},
            {'trigger': 'wait', 'source': 'walking', 'dest': 'idle', 'before': 'stop_move'},
            {'trigger': 'turn_left', 'source': 'idle', 'dest': 'turning_left', 'before': 'rotate_left'},
            {'trigger': 'wait', 'source': 'turning_left', 'dest': 'idle', 'before': 'stop_move'},
            {'trigger': 'turn_right', 'source': 'idle', 'dest': 'turning_right', 'before': 'rotate_right'},
            {'trigger': 'wait', 'source': 'turning_right', 'dest': 'idle', 'before': 'stop_move'},
            {'trigger': 'back', 'source': 'idle', 'dest': 'walking_back', 'before': 'walk_back'},
            {'trigger': 'wait', 'source': 'walking_back', 'dest': 'idle', 'before': 'stop_move'},
            {'trigger': 'stop', 'source': 'rest', 'dest': 'end'},
            {'trigger': 'rest', 'source': 'idle', 'dest': 'rest', 'before': 'crouch'},
            {'trigger': 'go', 'source': 'rest', 'dest': 'idle', 'before': 'wake_up'}
            ]

    machine = Machine(model=nao, states=states, transitions=transitions,
            initial='idle', ignore_invalid_triggers=True)

    run = True
    while run:
        try:
            key = stdscr.getkey()
        except:
            key = None

        if key == 'b':
            nao.back()

        elif key == 'c':
            nao.rest()

        elif key == 'g':
            nao.go()

        elif key == 'l':
            nao.turn_left()

        elif key == 'r':
            nao.turn_right()

        elif key == 's':
            nao.stop()

        elif key == 'w':
            nao.wait()

        if nao.state == 'end':
            run = False
        if nao.state == 'walking':
            nao.avoid_obstacle()
        time.sleep(0.1)




if __name__ == '__main__':
    curses.wrapper(main)
