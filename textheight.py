import cv2
import numpy as np

# Demo does not line up with top of frame
frame = np.zeros((128, 230, 3), np.uint8)
text = "Demo"
(tw, th), base = cv2.getTextSize(str(text), cv2.FONT_HERSHEY_PLAIN, 1, 1)
cv2.putText(frame, str(text), (0,th), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1, cv2.LINE_8)
cv2.imshow("Demo", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Demo does line up with top of frame (adjusted by 2 pixels)
frame = np.zeros((128, 230, 3), np.uint8)
text = "Demo"
(tw, th), base = cv2.getTextSize(str(text), cv2.FONT_HERSHEY_PLAIN, 1, 1)
cv2.putText(frame, str(text), (0,th+2), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1, cv2.LINE_8)
cv2.imshow("Demo", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()