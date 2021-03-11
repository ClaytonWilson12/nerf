#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
#import matplotlib.pylab as plt
import numpy as np 
#import pylab as pl
import time
import pyrealsense2 as rs

IMAGE_H = int(480)
IMAGE_W = int(848)
CAMERA_OFFSET = .02

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth, IMAGE_W, IMAGE_H, rs.format.z16,30)

# function to calculate depth based on (width or X direction, height or Y direction)
def get_depth(x, y):

    # offset = calibrate()
    count = 0
    distance_value = 0
     
    profile = pipeline.start(config)
    
    try:
        while count < 1:
	#while True:
            frames = pipeline.wait_for_frames()
            depth = frames.get_depth_frame()
            if not depth:
                continue
            
            width = depth.get_width()
            height = depth.get_height()

            distance = depth.get_distance(x, y)
            actual_distance = distance - CAMERA_OFFSET # offset distance for camera calibration
	        #print (actual_distance * 3.28)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
            count = count + 1

        return actual_distance
            
    finally:
        pipeline.stop()


def calibrate():

    distance_array = []
     
    profile = pipeline.start(config)
    
    try:
        while True:
            frames = pipeline.wait_for_frames()
            depth = frames.get_depth_frame()
            if not depth:
                continue
            
            width = depth.get_width()
            height = depth.get_height()

            distance = depth.get_distance(width / 2, height / 2)

            distance_array.append(distance)

            if (len(distance_array) > 50):
                break
    
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()

        
        avg = sum(distance_array)/len(distance_array)
        offset = (avg - 1.8492)
        print (offset)
        print (offset)
        return offset          
    finally:
        pipeline.stop()

if __name__ == "__main__":
    get_depth(300, 240)

cv2.destroyAllWindows()


