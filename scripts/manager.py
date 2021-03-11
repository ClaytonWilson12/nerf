import os
import time

#
arrayOfScripts = ["socket_server.py", "live_camera_filter.py", "actuator.py", ]

# os.system("cd /home/nerf/Desktop/test_ros/src/package1")
os.system("gnome-terminal -- roscore")

time.sleep(7)

for script in arrayOfScripts:
    os.system('gnome-terminal -x bash -c "python ' + '/home/nerf/Desktop/test_ros/src/package1/scripts/' + script + '; exec bash"')
    print("ran: " + script)

