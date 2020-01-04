import os
import cv2
import numpy as np
import pygame
from pygame.locals import *

def cv2pg(frame_yx_bgr):
    frame_yx_rgb = cv2.cvtColor(frame_yx_bgr, cv2.COLOR_BGR2RGB)
    frame_xy_rgb = frame_yx_rgb.swapaxes(0,1)
    return frame_xy_rgb
    

try:
    path = 'Smallville - S01E01 - Pilot.mkv'
    thumbpath = f"{os.path.splitext(path)[0]}.thumb.avi"
    thumb = cv2.VideoCapture(thumbpath)
    thumbw = int(thumb.get(cv2.CAP_PROP_FRAME_WIDTH))
    thumbh = int(thumb.get(cv2.CAP_PROP_FRAME_HEIGHT))

    pygame.init()
    pygame.display.set_caption("Scrubber")
    screen = pygame.display.set_mode([thumbw,thumbh])

    thumb.set(cv2.CAP_PROP_POS_FRAMES, 20000)
    running = True
    while(running):
        ret, frame = thumb.read()
        pygame.surfarray.blit_array(screen, cv2pg(frame))
        pygame.display.update() 
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        
finally:
    thumb.release()
    #pygame.quit()
    #cv2.destroyAllWindows()

    
# 0,0  0,1
#
# 1,0  1,1
#        frame[  0][  0] =    Top Left  [ 94,  96, 153]
#        frame[  0][229] =    Top Right [222, 211, 189]
#        frame[127][  0] = Bottom Left  [144, 113,  95]
#        frame[127][229] = Bottom Right [ 80,  47,  30]

# 0,1  0,0
#
# 1,1  1,0
#       fliplr[  0][  0] =    Top Right [222, 211, 189]
#       fliplr[  0][229] =    Top Left  [ 94,  96, 153]
#       fliplr[127][  0] = Bottom Right [ 80,  47,  30]
#       fliplr[127][229] = Bottom Left  [144, 113,  95]

# 0,0  1,0
#
# 0,1  1,1
# fliplr_rot90[  0][  0] =    Top Left  [ 94,  96, 153]
# fliplr_rot90[  0][127] = Bottom Left  [144, 113,  95]
# fliplr_rot90[229][  0] =    Top Right [222, 211, 189]
# fliplr_rot90[229][127] = Bottom Right [ 80,  47,  30]