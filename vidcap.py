from itertools import count
from pathlib import Path
import pygame
from pygame.locals import *
import numpy as np
import cv2
from usbpowermate import Powermate

def nextPath(path):
    for n in count():
        new_path = path.with_suffix(f'.{n}.png')
        if not new_path.exists():
            break
    return new_path

def clamp(val, minval, maxval):
    return max(minval, min(val, maxval))
    
def humanBytes(b):
    units = ["B", "KB", "MB", "GB", "TiB", "PiB", "EiB", "ZiB", "YiB"]
    for p, unit in enumerate(units):
        if b / 1024**p < 1024:
            break
    return f"{b/1024**p:.2f}{unit}"
        
def showHeader(frames, w, h, fps, rawsize):
    print(f"{frames} frames of {w}x{h} @ {fps:0.3f}fps ({humanBytes(rawsize)})")
    
class Metavideo():
    def __init__(self, vid):
        self.vid = vid
        self._w = None
        self._h = None
        self._size = None
        self._fps = None
        self._maxframe = None
        
    @property
    def w(self):
        if self._w is None:
            self._w = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        return self._w
        
    @property
    def h(self):
        if self._h is None:
            self._h = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return self._h
        
    @property
    def size(self):
        if self._size is None:
            self._size = (self.w, self.h)
        return self._size
        
    @property
    def fps(self):
        if self._fps is None:
            self._fps = self.vid.get(cv2.CAP_PROP_FPS)
        return self._fps
    
    @property
    def maxframe(self):
        if self._maxframe is None:
            self._maxframe = int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
        return self._maxframe
    
    @property
    def frame(self):
        return int(self.vid.get(cv2.CAP_PROP_POS_FRAMES))
    
    @frame.setter
    def frame(self, f):
        self.vid.set(cv2.CAP_PROP_POS_FRAMES, min(f, self.maxframe))
    
    @property
    def time(self):
        return self.vid.get(cv2.CAP_PROP_POS_MSEC)
        
    def showProgress(self):
        barlen = 79 - len("123456.00/: 12345678ms ") - len(str(self.maxframe))
        progress = int((self.frame / self.maxframe) * barlen)
        remaining = barlen - progress
        bar = (progress * "=") + (remaining * "-")
        #"123456/123456: 12345678ms "
        print(f"{self.frame:>6}/{self.maxframe}: {int(self.time):>8}ms {bar}", end="\r")

TOP = 0
MIDDLE = 1
BOTTOM = 2
LEFT = 0
RIGHT = 2
def write(frame, text, horz=MIDDLE, vert=MIDDLE, color=(255,255,255)):
    h, w, _ = frame.shape
    (tw, th), base = cv2.getTextSize(str(text), cv2.FONT_HERSHEY_PLAIN, 1, 1)
    if horz == LEFT:
        x = 0
    elif horz == MIDDLE:
        x = int((w-tw) / 2)
    elif horz == RIGHT:
        x = w-tw
    if vert == TOP:
        y = th+2
    elif vert == MIDDLE:
        y = int((h-(th+2)) / 2)
    elif vert == BOTTOM:
        y = h-(th+2)
    cv2.putText(frame, str(text), (x,y), cv2.FONT_HERSHEY_PLAIN, 1, color, 1, cv2.LINE_AA)

def cv2pg(frame_yx_bgr):
    frame_yx_rgb = cv2.cvtColor(frame_yx_bgr, cv2.COLOR_BGR2RGB)
    frame_xy_rgb = frame_yx_rgb.swapaxes(0,1)
    return frame_xy_rgb
    
def scrub(cap, path, pm):
    clock = pygame.time.Clock()
    running = True
    meta = Metavideo(cap)
    currframe = 0
    ret, frame = cap.read()
    pygame.display.set_caption("Scrubber")
    screen = pygame.display.set_mode(meta.size)
    while(cap.isOpened() and running):
        rate = 0
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.unicode == "q":
                    running = False
                elif event.key == K_LEFT:
                    rate += -1
                elif event.key == K_RIGHT:
                    rate += 1
        rate += pm.get_rotation()
        pressed = pm.get_pressed()
        mods = pygame.key.get_mods()
        mult = 1
        if mods & KMOD_SHIFT:
            mult *= 4
        if mods & KMOD_CTRL:
            mult *= 16
        rate *= mult
        currframe += rate
        currframe = clamp(currframe, 0, meta.maxframe)
        if pressed:
            cv2.imwrite(str(nextPath(path)), frame)
    
        
        meta.frame = currframe
        ret, new_frame = cap.read()
        if ret:
            frame = new_frame
            
        out_frame = frame.copy()
        write(out_frame, f"{currframe+1}/{meta.maxframe+1}", RIGHT, TOP)
        pygame.surfarray.blit_array(screen, cv2pg(out_frame))
        pygame.display.update()
        
        #capmeta.showProgress()
        
        clock.tick(meta.fps)
    
def main():
    path = Path(r'C:\Users\nfearnley\Desktop\gay\Horrifying Conversation.. A MOTHER ACCUSES HER SON OF BEING GAY AND ADDS HER REACTION AS IF HE WERE.mp4')
    cap = cv2.VideoCapture(str(path))
    pygame.init()
    pm = Powermate.find()[0]
    pm.open()
    try:
        scrub(cap, path, pm)
    finally:
        print()
        pm.close()
        cap.release()
        pygame.quit()
        cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()
