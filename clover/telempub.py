import rospy
from clover import srv
from std_msgs.msg import Float32MultiArray


get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
pub = rospy.Publisher('TELEMETRY', Float32MultiArray, queue_size=1)


if __name__ == '__main__':
    rospy.init_node("telem_topic")
    rate = rospy.Rate(1)

    
    while not rospy.is_shutdown():
        t = get_telemetry(frame_id='aruco_map')
        msgs = [t.x, t.y, t.z, t.voltage, float(t.armed)]
        array = Float32MultiArray(data=msgs)
        pub.publish(array)
        rate.sleep()
