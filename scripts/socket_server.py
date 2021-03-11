import socket
import select
import rospy
from std_msgs.msg import String

class Connect(object):

    def __init__(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except:
            print('socket cannot be created')
        server_address = ('10.0.1.5', 7800)
        self.sock.bind(server_address)
        self.sock.listen(1)
        print('listening on: ', server_address)

    def listen(self):

        #publisher for color picker
        pub_color = rospy.Publisher("color_choice", String, queue_size=10)
        rospy.init_node("simulate", anonymous=True)
        rate = rospy.Rate(10)

        #publisher for arm/disarm
        pub_arm = rospy.Publisher("arm_disarm", String, queue_size=10)
        rospy.init_node("simulate", anonymous=True)
        rate = rospy.Rate(10)

        while not rospy.is_shutdown():
            connection, client_address = self.sock.accept()
            print('')
            print('message received:')
            try:
                data = connection.recv(16)
                print(data)

                if(data == "armed" or data == "disarmed"):
                    pub_arm.publish(data)
                else:
                    pub_color.publish(data)
                
                
            finally:
                connection.close()
        	


def main():
    connect = Connect()
    connect.listen()

if __name__=='__main__':
    main() 

