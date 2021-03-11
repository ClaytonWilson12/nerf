import cv2
import numpy as np 
import rospy
import imutils
import time
import pyrealsense2 as rs
from std_msgs.msg import String
from servo_actuator_instruction import *
import pyrealsense2 as rs

MIN_RADIUS = 35
MAX_DEPTH = 4.572
MIN_DEPTH = 1.524
METERS_TO_FEET = 3.28

IMAGE_H = int(480)
IMAGE_W = int(848)
colorPicker = "red"

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, IMAGE_W, IMAGE_H, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, IMAGE_W, IMAGE_H, rs.format.z16, 30)

align_to = rs.stream.color
align = rs.align(align_to)

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

def get_depth(x,y):
    # offset = calibrate()
    count = 0
    distance_values = []

    frames = pipeline.wait_for_frames()
    aligned_frames = align.process(frames)
    depth = aligned_frames.get_depth_frame()
            
    width = depth.get_width()
    height = depth.get_height()

    distance = depth.get_distance(x, y)
    actual_distance = distance - .02 # offset distance for camera calibration
    
    if actual_distance > 0:
        distance_values.append(actual_distance)
            
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
    count = count + 1

    return actual_distance

def show():
    profile = pipeline.start(config)
    rospy.init_node('camera', anonymous=True)
    rospy.Subscriber("color_choice", String, callback)
    

    # publisher that sends instructions to motor.py file
    motor_publisher = rospy.Publisher('motorMessage', String, queue_size=10)
    actuator_publisher = rospy.Publisher('actuatorMessage', String, queue_size=10)
    y_inches = 0

    red = "red"
    blue = "blue"
    green = "green"    

    try:
        while not rospy.is_shutdown():

            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()

            color_image = np.asanyarray(color_frame.get_data())         
        
            #cv2.imshow('Color image', color_image)  
            filterImage = detectRed(color_image)
            global colorPicker
            if colorPicker == red:
                filterImage = detectRed(color_image) 
            elif colorPicker == blue:
                filterImage = detectBlue(color_image)

            elif colorPicker == green:
                filterImage = detectGreen(color_image)
            else:
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

                centerDepth = get_depth(int(x), int(y))
                #print (x)
                #print (y)
            else:
                x = 69
                y = 69
            
            if radius > MIN_RADIUS and MAX_DEPTH > centerDepth > MIN_DEPTH:
                cv2.circle(color_image, (int(x), int(y)), int(radius), (0,255,255), 2)
                cv2.circle(color_image, (int(x), int(y)), 5, (0,0,255), 2)

                # find how far target is from center x and send instructions to motor
                x_diff = move_x(x)
                direction = find_direction(x_diff)
                angle = calc_angle(x_diff)
                angle = int(angle) * int(direction)
                
                if (angle is not 0):
                    motor_publisher.publish(str(angle))
                print ("move motor:")
                print (angle)
                    
                

                # find how far target is from center y and send instructions to actuator
                if y_inches != (move_y(y)):
                    y_inches = move_y(y)
                    actuator_publisher.publish(str(y_inches))
                    print ("move actuator")
                    print (y_inches)

                
            else:
                cv2.circle(color_image, (int(x), int(y)), int(radius), (255,0,0), 2)
    

            cv2.imshow("final", color_image)
            #rospy.spin

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

    finally:
        pipeline.stop()
    return 0

show()

cv2.destroyAllWindows()
