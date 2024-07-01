import cv2
import numpy as np
import mediapipe as mp
import pyautogui

# top left, top right, bottom left, bottom right
pts = [(0,0),(0,0),(0,0),(0,0)]
pointIndex = 0
cx,cy = pyautogui.size()
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW) 

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

_,img = cam.read()
_,img = cam.read()


ASPECT_RATIO = (cy,cx)

pts2 = np.float32([[0,0],[ASPECT_RATIO[1],0],[0,ASPECT_RATIO[0]],[ASPECT_RATIO[1],ASPECT_RATIO[0]]])

# mouse callback function
def draw_circle(event,x,y,flags,param):
	global img
	global pointIndex
	global pts

	if event == cv2.EVENT_LBUTTONDBLCLK:
		cv2.circle(img,(x,y),0,(255,0,0),-1)
		pts[pointIndex] = (x,y)
		pointIndex = pointIndex + 1

def selectFourPoints():
	global img
	global pointIndex

	print ("Double-click on each of the four spots in the following order to choose them: top left, top right, bottom left, and bottom right.")


	while(pointIndex != 4):
		cv2.imshow('image',img)
		key = cv2.waitKey(20) & 0xFF
		if key == 27:
			return False

	return True


cv2.imshow('image',_)
cv2.setMouseCallback('image',draw_circle)



def tracking(video):
    
    hsv = cv2.cvtColor(video, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY)
    lower_red = np.array([0, 0, 10])
    upper_red = np.array([255, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(mask)
    (minValG, maxValG, minLocG, maxLocG) = cv2.minMaxLoc(gray)
    #cv2.circle(video, maxLoc, 10, (0, 255, 0), 1, cv2.LINE_AA)
    #cv2.circle(video, maxLocG, 10, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.imshow('Track Laser', video)
    red_x, red_y = maxLocG
    print(red_x, red_y)
    pyautogui.moveTo(red_x,red_y ,duration =0 )





while(1):
	if(selectFourPoints()):

		# The four points of  the image
		pts1 = np.float32([\
			[pts[0][0],pts[0][1]],\
			[pts[1][0],pts[1][1]],\
			[pts[2][0],pts[2][1]],\
			[pts[3][0],pts[3][1]] ])

		M = cv2.getPerspectiveTransform(pts1,pts2)
        
		while(1):

			_,frame = cam.read()

            

			dst = cv2.warpPerspective(frame,M,(cx,cy))
			tracking(dst)
            
            
			key = cv2.waitKey(10) & 0xFF
			if key == 27:
				break
	else:
		print ("Exit")

	break
	
cam.release()
cv2.destroyAllWindows()
