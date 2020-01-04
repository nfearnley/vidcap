import cv2
import numpy as np

frame = np.zeros((480,640,3), np.uint8)
cv2.imshow('frame', frame)

key = 0
while(key != 27):
    key = cv2.waitKeyEx()
    print(key)

#7340032 F1
#7405568 F2
#7471104 F3
#7536640 F4
#7602176 F5
#7667712 F6
#7733248 F7
#7798784 F8
#7864320 F9
#7929856 F10
#7995392 F11
#8060928 F12

#2490368 Up
#2621440 Down
#2424832 Left
#2555904 Right

#2949120 Insert
#2359296 Home
#2162688 Page Up
#3014656 Delete
#2293760 End
#2228224 Page Down



