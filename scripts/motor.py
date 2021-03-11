#import rospy
import time
import Jetson.GPIO as GPIO
#from std_msgs.msg import String

# Time to needed to move 40 degrees in 1 second
TIME = 0.05

STEP_PIN = 23
DIRECTION_PIN = 21
ENABLE_PIN = 19

def init():
    # GPIO setup
    GPIO.setmode(GPIO.BOARD)

    # motor pins
    GPIO.setup(ENABLE_PIN, GPIO.OUT, initial=GPIO.LOW)  # enable
    GPIO.setup(STEP_PIN, GPIO.OUT)  # step
    GPIO.setup(DIRECTION_PIN, GPIO.OUT)  # direction


def cleanup():

    GPIO.setup(ENABLE_PIN, GPIO.HIGH)  # enable
    GPIO.setup(STEP_PIN, GPIO.LOW)  # step
    GPIO.setup(DIRECTION_PIN, GPIO.LOW)  # direction

    GPIO.cleanup()


def setEnable(state):
    # enable motor
    if state == 0:
        GPIO.output(ENABLE_PIN, GPIO.LOW)
        msg = 'Disabled'

    # disable motor
    elif state == 1:
        GPIO.output(ENABLE_PIN, GPIO.HIGH)
        msg = 'Enabled'

    else:
        msg = 'Error: not valid Enable state (0-1)'

    #rospy.loginfo('Motor Enable: ' + msg)


def step():
    global SPEED
    # motor step
    GPIO.output(STEP_PIN, GPIO.HIGH)
    time.sleep(TIME)
    GPIO.output(STEP_PIN, GPIO.LOW)
    time.sleep(TIME)


def setDirection(state):
    # motor left
    if state == 0:
        GPIO.output(DIRECTION_PIN, GPIO.LOW)
        msg = 'Counterclockwise'

    # motor right
    elif state == 1:
        GPIO.output(DIRECTION_PIN, GPIO.HIGH)
        msg = 'Clockwise'

    else:
        msg = 'Error: not valid Direction state (0-1)'

    #rospy.loginfo('Motor Direction: '+ msg)


def moveMotor(data):
    #rospy.loginfo('Moving Motor...')
    print('moving motor...')

    # full step
    stepAmount = int(data / 1.80)

    for i in range(0, stepAmount):
        step()


    #rospy.loginfo('Motor Moved')
    print('motor moved')


def callback(msg):
    #rospy.loginfo("Received: " + msg.data)
    msgData = float(msg.data)

    try:    
        # move motor based on number given
        if msgData > 0:
            setDirection(0)
        else:
            setDirection(1)
    except:
        return 0
    # except ValueError:
        # rospy.loginfo('Motor: Error: data must be an float ' + msgData)

    moveMotor(msgData)


def listener():
    init()
    #rospy.init_node('motor', anonymous=True)
    #rospy.Subscriber('motorMessage', String, callback)
    #rospy.spin()


def motor_test():
    # test commands
    setDirection(0)
    moveMotor(80)
    setDirection(1)
    moveMotor(40)

    
def get_average_time(degrees, trials):
    # computes the average time to move X degrees with TRIALS amount of runs
    times = []
    for i in range(0, trials):
        setDirection(i%2)
        start = time.time()
        moveMotor(degrees)
        stop = time.time()
        times.append(stop-start)

    average_time = 0
    for i in range(0, len(times)):
        average_time = average_time + times[i]
    average_time = average_time / trials
    print(average_time)


if __name__ == '__main__':
    #listener()
    init()

    motor_test()
    cleanup()
    
