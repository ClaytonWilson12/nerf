import rospy
import time
import Jetson.GPIO as GPIO
from std_msgs.msg import String


FLYWHEEL_PIN = 29
#TRIGGER_PIN = 23
WAIT_FLYWHEEL = 1       # wait for flywheel before activating trigger
SHOOT_TIME = 1          # time to shoot 1 dart
TEST = True            # Test Mode

def init():
    # GPIO setup
    GPIO.setmode(GPIO.BOARD)

    # nerf gun pins
    GPIO.setup(FLYWHEEL_PIN, GPIO.OUT, initial=GPIO.LOW)  # Relay 1
    #GPIO.setup(TRIGGER_PIN, GPIO.OUT, initial=GPIO.LOW)  # Relay 2

# reset pins
def reset():
    GPIO.output(FLYWHEEL_PIN, GPIO.LOW)
    #GPIO.output(TRIGGER_PIN, GPIO.LOW)  

    if(TEST == True):
        print('Gun: Flywheel: Deactivated')

def activateFlywheel():
    GPIO.output(FLYWHEEL_PIN, GPIO.HIGH)
    if(TEST == True):
        print('Gun: Flywheel: Activated')

def activateTrigger():
    #GPIO.output(TRIGGER_PIN, GPIO.HIGH)
    if(TEST == True):
        print('Gun: Trigger: Activated')

def shoot(data):
    if(TEST == False):
        # activate flywheel for WAIT_FLYWHEEL seconds
        activateFlywheel()
        time.sleep(WAIT_FLYWHEEL*data)

        # activate trigger for SHOOT_TIME seconds
        # activateTrigger()
        # time.sleep(SHOOT_TIME * data)

    else:
        activateFlywheel()
        time.sleep(WAIT_FLYWHEEL*data)

        # activate trigger for SHOOT_TIME seconds
        # activateTrigger()
        # time.sleep(SHOOT_TIME * data)

    # turn off trigger and flywheel
    rospy.loginfo('Gun: Shot ' + str(data) + ' Times')
    if(TEST == True):
        print('Gun: Shot ' + str(data) + ' Times')
    reset()

def callback(data):
    try:
        msgData = int(data.data)
        shoot(msgData)
    except ValueError:
        rospy.loginfo('Gun: Error: data must be an int ' + data)
    except:
        return 0


def listener():
    init()
    rospy.init_node('gun', anonymous=True)
    rospy.Subscriber('gunMessage', String, callback)
    rospy.spin()


def gunTest():
    # runs test for nerf gun
    init()
    shoot(10)

if __name__ == "__main__":
    if(TEST == True):
        gunTest()
    else:
        listener()
