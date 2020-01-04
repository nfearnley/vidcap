import pygame
from pygame.locals import *
    
def pygameTest(screen):
    running = True
    blink = False
    black = [0,0,0]
    white = [255,255,255]
    while(running):
        blink = not blink
        screen.fill(white if blink else black)
        pygame.display.flip()        
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                running = False

def main():
    w = 1280
    h = 768
    pygame.init()
    pygame.display.set_caption("pygameTest")
    screen = pygame.display.set_mode([w,h])
    try:
        pygameTest(screen)
    finally:
        pygame.quit()
    
if __name__ == "__main__":
    main()
