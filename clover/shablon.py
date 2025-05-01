import rospy
from clover import srv
from std_srvs.srv import Trigger
from clover.srv import SetLEDEffect
import cv2 as cv
from std_msgs.msg import Int16
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np
from mavros_msgs.srv import CommandBool
import math


get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
arming = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)
srv_land = rospy.ServiceProxy('land', Trigger)

rospy.init_node('flight')
bridge = CvBridge()
state = rospy.Publisher('DATA_INT', Int16, queue_size=1)


def land():
    navigate_wait(1, 1, 1)
    set_position(frame_id='aruco_69', z=0.7, speed=0.2)
    rospy.sleep(0.2)
    set_position(frame_id='aruco_69', z=0.5, speed=0.2)
    rospy.sleep(0.2)
    srv_land()
    rospy.sleep(3)
    arming(False)


def navigate_wait(x=0, y=0, z=1.5, yaw=float('nan'), speed=0.5, frame_id='aruco_map', auto_arm=False, tolerance=0.2):
    navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)


def home(msg): #Home
    if msg.data == 1:
        state.publish(data=2)
        print('HOME')
        rospy.on_shutdown(start)
        navigate_wait(0, 0, speed=1)
        land()
        state.publish(data=1)


#Secret function for frontend
def start(msg):
    if msg.data == 2:
        state.publish(data=2)
        rospy.on_shutdown(home)
        navigate_wait(frame_id='body', auto_arm=True)
        navigate_wait(3.95, 0.4, 1)
        navigate_wait(0.5, 3, 1)
        navigate_wait(6.45, 3.4, 1)
        land()
        print("Done, wait...")
        rospy.sleep(5)
        state.publish(data=1)
        print("Ready to call ")


#Start programm
if __name__ == '__main__':
    state.publish(data=1)
    print('Ready to work')
    rospy.Subscriber('DATA_INT', Int16, start)
    rospy.Subscriber('HOME', Int16, home)
    rospy.spin()

