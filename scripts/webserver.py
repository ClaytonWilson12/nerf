from flask import Flask, render_template, Response
from cv_bridge import CvBridge
import numpy as np 
import time
import cv2


import pyrealsense2 as rs
# export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python2.7/pyrealsense2

app = Flask(__name__)

IMAGE_H = int(480)
IMAGE_W = int(848)

pipeline = rs.pipeline()
config = rs.config()
#config.enable_stream(rs.stream.depth, DEPTH_W, DEPTH_H, rs.format.z16, 30)
config.enable_stream(rs.stream.color, IMAGE_W, IMAGE_H, rs.format.bgr8, 30)


def gen_frames():  # generate frame by frame from camera
    profile = pipeline.start(config)

    while True:
        # Capture frame-by-frame
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue
        color_image = np.asanyarray(color_frame.get_data())   
        
        ret, buffer = cv2.imencode('.jpg', color_image)
        frames = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frames + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host="10.74.0.20", port=8080)








