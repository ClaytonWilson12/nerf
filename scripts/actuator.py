import rospy
import time
import Jetson.GPIO as GPIO
from std_msgs.msg import String


# Max Extend Time: roughly 1.185s
# Max Retract Time: roughly 1.085s
height = 0
MAX_HEIGHT = 10
MAX_HEIGHT_TIME = 1.185
EXTEND_SPEED = (MAX_HEIGHT/MAX_HEIGHT_TIME)
MIN_HEIGHT_TIME = MAX_HEIGHT_TIME #1.085
RETRACT_SPEED = (MAX_HEIGHT/MIN_HEIGHT_TIME)

RELAY_1_PIN = 31
RELAY_2_PIN = 33

TEST = False        # Test Mode

def init():
    # GPIO setup
    GPIO.setmode(GPIO.BOARD)

    # actuator pins
    GPIO.setup(RELAY_1_PIN, GPIO.OUT, initial=GPIO.LOW)  # Relay 1
    GPIO.setup(RELAY_2_PIN, GPIO.OUT, initial=GPIO.LOW)  # Relay 2


def cleanup():
    GPIO.output(RELAY_1_PIN, GPIO.LOW)
    GPIO.output(RELAY_2_PIN, GPIO.LOW)

    GPIO.cleanup()


def extend(data):
    # data represents the time to move in seconds
    # output 10 (Make sure that the Relay 2 is low before setting Relay 1 high)
    global height
    global MAX_HEIGHT_TIME
    global EXTEND_SPEED

    # cap data to MAX_HEIGHT
    if data > MAX_HEIGHT:
        data = MAX_HEIGHT
    
    # figure out what max_data can be
    time_required = data * (1 / EXTEND_SPEED)

    GPIO.output(RELAY_2_PIN, GPIO.LOW)
    GPIO.output(RELAY_1_PIN, GPIO.HIGH)  

    time.sleep(time_required)

    #output 00
    GPIO.output(RELAY_1_PIN, GPIO.LOW)
    GPIO.output(RELAY_2_PIN, GPIO.LOW)
    rospy.loginfo('Actuator: extended: ' + str(data))
    
    height = round(height + data, 3)
    if (TEST == True):
        print('Actuator: current height: ' + str(height))


def retract(data):
    # data represents the time to move in seconds
    # output 01 (Make sure that the Relay 1 is low before setting Relay 2 high)
    global height
    global MIN_HEIGHT_TIME
    global RETRACT_SPEED

    # cap data to MAX_HEIGHT
    if data > MAX_HEIGHT:
        data = MAX_HEIGHT

    time_required = data * (1 / RETRACT_SPEED)

    GPIO.output(RELAY_1_PIN, GPIO.LOW)
    GPIO.output(RELAY_2_PIN, GPIO.HIGH)
        
    time.sleep(time_required)

    #output 00
    GPIO.output(RELAY_1_PIN, GPIO.LOW)
    GPIO.output(RELAY_2_PIN, GPIO.LOW)

    height = round(height - data, 3)
    rospy.loginfo('Actuator: retracted: ' + str(data))

    if(TEST == True):
        print('Actuator: current height: ' + str(height))


def setHeight(data):
    # if data > (height + .25):
    if data > height:
        extend(data - height)
    
    # elif data < (height - .25)
    elif data < height:
        retract(height - data)


def callback(msg):
    rospy.loginfo("Received: " + msg.data)

    try:
        msgData = float(msg.data)
        setHeight(msgData)
    except ValueError:
        rospy.loginfo('Actuator: Error: data must be an float ' + msgData)
    except:
        return 0

def listener():
    global height
    init()
    height = 10
    retract(MAX_HEIGHT)
    rospy.init_node('actuator', anonymous=True)
    rospy.Subscriber('actuatorMessage', String, callback)
    rospy.spin()


def actuatorTest():
    # runs test for actuator
    global height
    init()
    
    # reset location
    height = 10
    setHeight(0)

    # wait 1 seoond for next command
    time.sleep(1)
    avg_time = 0
    TRIALS = 1
    for i in range(0, TRIALS):
        setHeight(0)
        start = time.time()
        setHeight(8)
        stop = time.time()
        avg_time = avg_time + (stop - start)
    avg_time = avg_time / TRIALS
    print("Average Time: " + str(round(avg_time, 4)))


if __name__ == '__main__':
    if(TEST == True):
        actuatorTest()
    else:
        listener()
