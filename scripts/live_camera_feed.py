
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Histograms for row detection
"""
#%% Import section
#files

import cv2
#import matplotlib.pylab as plt
import numpy as np 
#import pylab as pl
import time
import pyrealsense2 as rs
from live_camera_depth import *

IMAGE_H = int(480)
IMAGE_W = int(848)
#DEPTH_H = 480
#DEPTH_W = 848

pipeline = rs.pipeline()
config = rs.config()
rs.align()
#config.enable_stream(rs.stream.depth, DEPTH_W, DEPTH_H, rs.format.z16, 30)
config.enable_stream(rs.stream.color, IMAGE_W, IMAGE_H, rs.format.bgr8, 30)



def show():

    profile = pipeline.start(config)
    
    try:
        while True:
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue

            color_image = np.asanyarray(color_frame.get_data())         

            centercoords = (100,300)
            color_image = cv2.circle(color_image, centercoords, 5, (0,0,255), -1)

            depth = get_depth(100, 300)
            print (depth * 3.28)

            cv2.imshow('Color image', color_image)   
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
            
    finally:
        pipeline.stop()

show()

cv2.destroyAllWindows()