#import rospy
import time
import Jetson.GPIO as GPIO
#from std_msgs.msg import String


def init():
    # GPIO setup
    GPIO.setmode(GPIO.BOARD)

    # actuator pins
    GPIO.setup(31, GPIO.OUT, initial=GPIO.LOW)  # Relay 1
    GPIO.setup(33, GPIO.OUT, initial=GPIO.LOW)  # Relay 2


def cleanup():
    GPIO.cleanup()


def extend(data):
    # data represents the time to move in seconds
    # output 10 (Make sure that the Relay 2 is low before setting Relay 1 high)
    GPIO.output(33, GPIO.LOW)   # Relay 2
    GPIO.output(31, GPIO.HIGH)   # Relay 1   

    time.sleep(data)

    #output 00
    GPIO.output(31, GPIO.LOW)    # Relay 1
    GPIO.output(33, GPIO.LOW)   # Relay 2
    #rospy.loginfo('Actuator: extended: ' + data)
    print('Actuator: extended: ' + str(data))
    
def retract(data):
    # data represents the time to move in seconds
    # output 01 (Make sure that the Relay 1 is low before setting Relay 2 high)
    GPIO.output(31, GPIO.LOW)     # Relay 1
    GPIO.output(33, GPIO.HIGH)   # Relay 2   
        
    time.sleep(data)

    #output 00
    GPIO.output(31, GPIO.LOW)    # Relay 1
    GPIO.output(33, GPIO.LOW)   # Relay 2

    #rospy.loginfo('Actuator: retracted: ' + data)
    print('Actuator: retracted: ' + str(data))

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

        elif command == 'extend':
            extend(float(data))

        elif command == 'retract':
            retract(float(data))
        else:
            return 0
        #else:
            #rospy.loginfo('Actuator: Error: not valid command ' + command)
            #rospy.loginfo('Commands are:\n init\n cleanup\n extend:[time in seconds]\n retract:[time in seconds]')
    except:
        return 0
    #except IndexError:
        #rospy.loginfo('Actuator: Error: no delimiter found ":" '+ msg)

    #except ValueError:
        #rospy.loginfo('Actuator: Error: data must be an float ' + msgData)

#def listener():
    #init()
    #rospy.init_node('actuator', anonymous=True)
    #rospy.Subscriber('actuatorMessage', String, callback)
    #rospy.spin()

if __name__ == '__main__':
    #listener()
    init()
    extend(5)
    retract(1)
