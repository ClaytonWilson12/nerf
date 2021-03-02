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

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16,30)

# function to calculate depth based on (width or X direction, height or Y direction)
def get_depth(x, y):

    # offset = calibrate()
    count = 0
    distance_values = []
     
    profile = pipeline.start(config)
    
    try:
        #while count < 5:
	while True:
            frames = pipeline.wait_for_frames()
            depth = frames.get_depth_frame()
            if not depth:
                continue
            
            width = depth.get_width()
            height = depth.get_height()

            distance = depth.get_distance(x, y)
            actual_distance = distance - .02 # offset distance for camera calibration
	    print (actual_distance * 3.28)
            if actual_distance > 0:
                distance_values.append(actual_distance)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
            count = count + 1

        average_distance = sum(distance_values) / len(distance_values)
        print (average_distance)
            
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
    get_depth(424, 240)

cv2.destroyAllWindows()


