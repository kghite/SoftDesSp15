""" Experiment with face detection and image filtering using OpenCV """

import cv2
import numpy as np

# Grab frames from screen
cap = cv2.VideoCapture(0)

# Get opencv filters
face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')
kernel = np.ones((21,21),'uint8')

while(True):
	# Edit face found in a frame
	ret, frame = cap.read()
	faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20,20))
	
	# Blur faces
	for (x,y,w,h) in faces:
		frame[y:y+h,x:x+w,:] = cv2.dilate(frame[y:y+h,x:x+w,:], kernel)
	# Draw a rectangle around faces   
	for (x,y,w,h) in faces:
	    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255))
	# Add a cartoon face over faces
	for (x,y,w,h) in faces:
		# Draw the eyes
		eye1_x = int(x + x/3)
		eye1_y = int(y + y/3)
		eye1_rad = int(x/8)
		cv2.circle(frame, (eye1_x, eye1_y), int(eye1_rad/2), (255,0,0), 4,8,0)
		cv2.circle(frame, (eye1_x, eye1_y), eye1_rad, (255,255,255), 8,8,0)
		eye2_x = int(x + 2*x/3)
		eye2_y = int(y + y/3)
		eye2_rad = int(x/8)
		cv2.circle(frame, (eye2_x, eye2_y), int(eye2_rad/2), (255,0,0), 4,8,0)
		cv2.circle(frame, (eye2_x, eye2_y), eye2_rad, (255,255,255), 8,8,0)
		# Draw the mouth
		mouth_x = x
		mouth_y = y
		cv2.ellipse(frame, (mouth_x+mouth_x/2, mouth_y+50+mouth_y/2), (x/2, y/2),0,0,180, 1, 8)

	# Display the resulting frame
	cv2.imshow('frame',frame) 
	if cv2.waitKey(1) & 0xFF == ord('q'):
	    break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()