import sys
import select 
import time 
import pygame

# draw a little area (to fucus on to get keys)


# key codes
# from : https://www.pygame.org/docs/ref/key.html

#print("hello")

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def getKey():
    #tty.setcbreak(sys.stdin.fileno())
    pygame.init()
    pygame.display.set_mode((100, 100))
    c='s'
    cok=False
    compteur=time.time()
    while not cok and time.time()-compteur< 2 :
        event = test()
        if event is not None:
            
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                c = event.key
                cok=True
        
    pygame.quit()
    
    return cok,c

def test() :
    L = pygame.event.get()
    if L != [] : return L[0]
    else : return None

#c=""
#while (c != "!"):
#    cok,c = getKey()
#    print(c)
#    time.sleep(0.1)

