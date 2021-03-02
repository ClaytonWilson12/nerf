#!/usr/bin/env python3
import rospy
import time
from std_msgs.msg import String
def simulate():
    pub = rospy.Publisher("color_choice", String, queue_size=10)
    rospy.init_node("simulate", anonymous=True)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        pub.publish("red")
        print "red"
        time.sleep(3)
        pub.publish("blue")
        print "blue"
        time.sleep(3)
        pub.publish("green")
        print "green"
        time.sleep(3)

        rate.sleep()
if __name__ == "__main__":
    simulate()
