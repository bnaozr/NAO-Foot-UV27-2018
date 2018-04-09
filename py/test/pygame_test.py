import pygame
import sys
pygame.init()

# draw a little area (to fucus on to get keys)
pygame.display.set_mode((100, 100))

# key codes
# from : https://www.pygame.org/docs/ref/key.html
#  K_UP                  up arrow
#  K_DOWN                down arrow
#  K_RIGHT               right arrow
#  K_LEFT                left arrow

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            #print event.type,event.key,pygame.K_w,pygame.K_s
            if event.key == pygame.K_UP:
                print('Forward')
            elif event.key == pygame.K_DOWN:
                print('Backward')
            elif event.key == pygame.K_LEFT:
                print('Left')
            elif event.key == pygame.K_RIGHT:
                print('Right')
