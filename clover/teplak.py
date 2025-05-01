import rospy
import cv2 as cv
import math
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import numpy as np

rospy.init_node('teplak')
bridge = CvBridge()

image_pub_jet = rospy.Publisher('Jet', Image, queue_size=1)
cap = cv.VideoCapture(1, cv.CAP_V4L)
cap.set(cv.CAP_PROP_CONVERT_RGB, 0.0)


while True:
        ret, frame = cap.read()
        imdata, thdata = np.array_split(frame, 2)
        bgr = cv.cvtColor(imdata, cv.COLOR_YUV2BGR_YUYV)
        bgr = cv.convertScaleAbs(bgr, alpha=1.0)
        bgr = cv.resize(bgr, (256, 192), interpolation=cv.INTER_CUBIC)
        colored_image = cv.applyColorMap(bgr, cv.COLORMAP_JET)
        img = cv.rotate(colored_image, cv.ROTATE_90_COUNTERCLOCKWISE)
        image_pub_jet.publish(bridge.cv2_to_imgmsg(img, 'bgr8'))
