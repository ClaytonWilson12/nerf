import cv2
import numpy as np 
import rospy
import imutils
import time
import pyrealsense2 as rs
from std_msgs.msg import String
from std_msgs.msg import Int16
from servo_instruction import *
from live_camera_depth import *

IMAGE_H = int(480)
IMAGE_W = int(848)
colorPicker = "blue"

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, IMAGE_W, IMAGE_H, rs.format.bgr8, 30)

def callback(data):
    print(data.data)
    rospy.loginfo(rospy.get_caller_id() + 'i heard %s', data.data) 
    global colorPicker
    colorPicker = str(data.data)
    if colorPicker == "red":
        print ("r")
    if colorPicker == "blue":
        print ("b")
    if colorPicker == "green":
        print ("g")
    #print(colorPicker)
    return 0

def detectRed(frame):
    lowerRed = np.array([170,100,50])
    upperRed = np.array([180,255,255])
    HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    filterRed = cv2.inRange(HSV, lowerRed, upperRed)
    return filterRed

def detectBlue(frame):
    lowerBlue = np.array([100,50,0])
    upperBlue = np.array([120,255,255])
    HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    filterBlue = cv2.inRange(HSV, lowerBlue, upperBlue)
    return filterBlue

def detectGreen(frame):
    lowerGreen = np.array([40,50,35])
    upperGreen = np.array([80,255,255])
    HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    filterGreen = cv2.inRange(HSV, lowerGreen, upperGreen)
    return filterGreen


def show():
    profile = pipeline.start(config)
    rospy.init_node('camera', anonymous=True)
    rospy.Subscriber("color_choice", String, callback)

    # publisher that sends instructions to motor.py file
    motor_publisher = rospy.Publisher('motorMessage', String, queue_size=10)

    red = "red"
    blue = "blue"
    green = "green"    


    try:
        while True:


            
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue


            color_image = np.asanyarray(color_frame.get_data())         
        
            #cv2.imshow('Color image', color_image)  
            filterImage = detectRed(color_image)
            global colorPicker
            if colorPicker == red:
                #print "hi red"
                filterImage = detectRed(color_image) 
            elif colorPicker == blue:
                #print "hi blue"
                filterImage = detectBlue(color_image)

            elif colorPicker == green:
                #print "hi green"
                filterImage = detectGreen(color_image) 
            
            else:
                #print "poop"
                filterImage = detectGreen(color_image) 

            cv2.imshow('Filtered Raw', filterImage)

            filterImage = cv2.erode(filterImage, None, iterations=1)
            filterImage = cv2.dilate(filterImage, None, iterations=1)
            #cv2.imshow('Filtered erode/dilate', filterImage)

            coordCenter = cv2.findContours(filterImage.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            coordCenter = coordCenter[0] if imutils.is_cv2() else coordCenter[1] 
            center = None

            radius = 0

            if len(coordCenter) > 0:
                cen = max(coordCenter, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(cen)
                M = cv2.moments(cen)
                center = (int(M["m10"] / M["m00"]), int(M["m00"] / M["m01"]))
                #if (radius > 30):
                    #print (x)
                    #print (y)
                    #print "_________"
                    #print (radius)

                
                
            
            if radius > 35 & (get_depth(x, y) > 1.524):
                cv2.circle(color_image, (int(x), int(y)), int(radius), (0,255,255), 2)
                cv2.circle(color_image, center, 5, (0,0,255), -1)
                cv2.circle(color_image, (int(x), int(y)), 5, (0,0,255), 2) 

                # find how far target is from center and send instructions to motor
                x_diff = move_x(x)
                direction = find_direction(x_diff)
                angle = calc_angle(x_diff)
                print (direction)
                print (angle)
                 

            cv2.imshow("final", color_image)
            #rospy.spin

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()

    finally:
        pipeline.stop()
    return 0

show()

cv2.destroyAllWindows()
