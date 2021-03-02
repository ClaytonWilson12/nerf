#import rospy
import time
import Jetson.GPIO as GPIO
#from std_msgs.msg import String


def init():
    # GPIO setup
    GPIO.setmode(GPIO.BOARD)

    # motor pins
    GPIO.setup(19, GPIO.OUT, initial=GPIO.LOW)  # enable (active low)
    GPIO.setup(21, GPIO.OUT)  # microstep 1
    GPIO.setup(23, GPIO.OUT)  # microstep 2
    GPIO.setup(29, GPIO.OUT)  # microstep 3
    GPIO.setup(31, GPIO.OUT, initial=GPIO.HIGH)  # rest (active low)
    GPIO.setup(33, GPIO.OUT, initial=GPIO.LOW)  # sleep (active low)
    GPIO.setup(35, GPIO.OUT)  # step
    GPIO.setup(37, GPIO.OUT)  # direction


def cleanup():
    GPIO.cleanup()


def setEnable(state):
    # enable motor
    if state == 1:
        GPIO.output(19, GPIO.LOW)
        msg = 'Enabled'

    # disable motor
    elif state == 0:
        GPIO.output(19, GPIO.HIGH)
        msg = 'Disabled'

    else:
        msg = 'Error: not valid Enable state (0-1)'

    #rospy.loginfo('Motor Enable: ' + msg)


def setMicrostep(state):
    # full step
    if state == 0:
        GPIO.output(21, GPIO.LOW)
        GPIO.output(23, GPIO.LOW)
        GPIO.output(29, GPIO.LOW)
        msg = 'full'

    # 1/2 step
    elif state == 1:
        GPIO.output(21, GPIO.HIGH)
        GPIO.output(23, GPIO.LOW)
        GPIO.output(29, GPIO.LOW)
        msg = '1/2'

    # 1/4 step
    elif state == 2:
        GPIO.output(21, GPIO.LOW)
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(29, GPIO.LOW)
        msg = '1/4'

    # 1/8 step
    elif state == 3:
        GPIO.output(21, GPIO.HIGH)
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(29, GPIO.LOW)
        msg = '1/8'

    # 1/16 step
    elif state == 4:
        GPIO.output(21, GPIO.HIGH)
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(29, GPIO.HIGH)
        msg = '1/16'

    else:
        msg = 'Error: not valid Microstep size (0-4)'

    #rospy.loginfo('Motor Microstep: ' + msg)


def setRest(state):
    # motor rest
    if state == 1:
        GPIO.output(31, GPIO.LOW)
        msg = 'True'

    # motor awake
    elif state == 0:
        GPIO.output(31, GPIO.HIGH)
        msg = 'False'

    else:
        msg = 'Error: not valid Rest state (0-1)'

    #rospy.loginfo('Motor Rest: ' + msg)


def setSleep(state):
    # motor sleep
    if state == 0:
        GPIO.output(33, GPIO.HIGH)
        msg = 'False'

    # motor awake
    elif state == 1:
        GPIO.output(33, GPIO.LOW)
        msg = 'True'

    else:
        msg = 'Error: not valid Sleep state (0-1)'

    #rospy.loginfo('Motor Sleep: '+ msg)


def step():
    # motor step
    GPIO.output(35, GPIO.HIGH)
    time.sleep(0.01)
    GPIO.output(35, GPIO.LOW)
    time.sleep(0.01)

def setDirection(state):
    # motor left
    if state == 0:
        GPIO.output(37, GPIO.LOW)
        msg = 'Counterclockwise'

    # motor right
    elif state == 1:
        GPIO.output(37, GPIO.HIGH)
        msg = 'Clockwise'

    else:
        msg = 'Error: not valid Direction state (0-1)'

    #rospy.loginfo('Motor Direction: '+ msg)


def moveMotor(data):
    #rospy.loginfo('Moving Motor...')
    print('moving motor...')

    # full step
    stepAmount = int(data / 1.80)
    data = data - (stepAmount * 1.80)
    setMicrostep(0)

    for i in range(0, stepAmount):
        step()

    # half step
    stepAmount = int(data / 0.90)
    data = data - (stepAmount * 0.90)
    setMicrostep(1)
    for i in range(0, stepAmount):
        step()

    # fourth step
    stepAmount = int(data / 0.45)
    data = data - (stepAmount * 0.45)
    setMicrostep(2)
    for i in range(0, stepAmount):
        step()

    # eighth step
    stepAmount = int(data / 0.225)
    data = data - (stepAmount * 0.225)
    setMicrostep(3)
    for i in range(0, stepAmount):
        step()
        
    # sixteenth step
    stepAmount = int(data / 0.1125)
    data = data - (stepAmount * 0.1125)
    setMicrostep(4)
    for i in range(0, stepAmount):
        step()

    #rospy.loginfo('Motor Moved')
    print('motor moved')

def callback(msg):
    #rospy.loginfo("Received: " + msg.data)
    msgData = msg.data

    try:
        parseIndex = msgData.index(':')
        command = msgData[:parseIndex]
        data = msgData[parseIndex + 1:]

        if command == 'init':
            init()

        elif command == 'cleanup':
            cleanup()

        elif command == 'setEnable':
            setEnable(int(data))

        elif command == 'setMicrostep':
            setMicrostep(int(data))

        elif command == 'setRest':
            setRest(int(data))

        elif command == 'setSleep':
            setSleep(int(data))

        elif command == 'step':
            step()

        elif command == 'setDirection':
            setDirection(int(data))

        elif command == 'moveMotor':
            moveMotor(float(data))

        else:
            #rospy.loginfo('Motor: Error: not valid command ' + command)
            #rospy.loginfo('Commands are:\n init\n cleanup\n setEnable[0/1]\n setMicrostep[0-4]\n setRest[0/1]\n setSleep[0/1]\n step\n setDirection[0/1]\n moveMotor[degrees]')
            print('not valid command')
    except IndexError:
        #rospy.loginfo('Motor: Error: no delimiter found ":" '+ msg)
        print('error')
    except ValueError:
        #rospy.loginfo('Motor: Error: data must be an int ' + msgData)
        print('error')

def listener():
    init()
    setSleep(0)
    #rospy.init_node('motor', anonymous=True)
    #rospy.Subscriber('motorMessage', String, callback)
    #rospy.spin()


if __name__ == '__main__':
    #listener()
    init()
    setSleep(0)
    moveMotor(180)
    cleanup()

