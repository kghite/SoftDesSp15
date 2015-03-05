import numpy as np
import cv2

cap = cv2.VideoCapture(0)

hand = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/hand_cascade.xml')

while(True):
	# Capture frame by frame
	ret, frame = cap.read()

	frame = cv2.flip(frame, 1)

	hands = hand.detectMultiScale(frame, scaleFactor=1.2, minSize=(20,20))

	for (x,y,w,h) in hands:
	    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255))

	cv2.rectangle(frame, (20, 30), (40, 50), (255, 0, 0), 20)

	# Display the resulting frame
	cv2.imshow('frame', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

	# Release the capture
cap.release()
cv2.destroyAllWindows()