from usbpowermate import Powermate
import pygame
from pygame.locals import *

def inrange(val, minval, maxval):
    return minval <= val <= maxval

def clamp(val, minval, maxval):
    return max(minval, min(val, maxval))
    
class PixDot():
    def __init__(self, pix, w=257, h=251, x=0, y=0, bg=0x000000, fg=0xFFFFFF):
        self.pix = pix
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.bg, self.fg = bg, fg
        
    def set(self, x, y):
        self.pix[self.x, self.y] = self.bg
        self.x, self.y = clamp(x, 0, self.w-1), clamp(y, 0, self.h-1)
        self.pix[self.x, self.y] = self.fg
        
    def move(self, dx, dy):
        self.set(self.x+dx, self.y+dy)
        
    @property
    def edge(self):
        return (self.x_edge, self.y_edge)
    
    @property    
    def x_edge(self):
        return self.x == 0 or self.x == self.w-1
    
    @property
    def y_edge(self):
        return self.y == 0 or self.y == self.h-1
    
def main():
    global z
    w, h = 257, 251
    dy = 1
    running = True
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Scrub Test")
    screen = pygame.display.set_mode([w,h])
    pix = pygame.surfarray.pixels2d(screen)
    pd = PixDot(pix, w, h)
    pm = Powermate.find()[0]
    pm.open()
    while running:
        dx = pm.get_rotation()
        if dx != 0:
            pd.move(dx, dy)
            if pd.y_edge:
                dy *= -1
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                    
        pygame.display.update()
        clock.tick(25)
    pygame.quit()
    pm.close()
    
if __name__ == "__main__":
    main()
