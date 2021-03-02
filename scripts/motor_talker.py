import rospy
from std_msgs.msg import String
# from std_msgs.msg import UInt8
import time

pub2 = rospy.Publisher('motorMessage', String, queue_size=10)


def callback(info):
    print(info.data)
    logic_output(info)


def logic():
    print("running logic file")
    rospy.init_node('logic', anonymous=True)
    # rospy.Subscriber("camera", UInt8, callback)

    logic_output('setDirection:0')
    logic_output('moveMotor:180')

    rospy.spin()


def logic_output(data):
    pub2.publish(data)


if __name__ == '__main__':
    logic()
