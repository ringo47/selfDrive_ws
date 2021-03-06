#!/usr/bin/env python

# Write subscriber to /front_camera/image_color and just publish to cv2.
# Look for calibration properties in Manual.
# Publish lane offsets and curvatures. -- DO THIS
# Locate and read /lane_fit /lane_fit /lane_planner /path_following nodes.
# See adding custom signs in Gazebo.
# Pipe YOLO.

# CHANGE XRES AND YRES PER PIXEL IN LINE FIT AND PIPE TEST.

import sys
import rospy
from cv2 import cv2 # To make PyLint recognize cv2
from std_msgs.msg import String
from std_msgs.msg import Float32
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from combined_thresh import combined_thresh
from combined_thresh2 import combined_thresh2
from perspective_transform import perspective_transform
from line_fit import line_fit, viz2, calc_curve, final_viz
from time import time
import os

image_topic = '/front_camera/image_color'
count = 0

class image_offset:

  def __init__(self):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber(image_topic,Image,self.callback)
    self.pub = rospy.Publisher("laneOffset", Float32, queue_size=10)

  def callback(self,data):
    global count
    try:
      img = self.bridge.imgmsg_to_cv2(data, desired_encoding = "rgb8")
      if img.dtype == 'float32':
        img = np.array(img)*255
        img = np.uint8(img)
      img, _, _, _, _ = combined_thresh(img)
      img, _, _, _ = perspective_transform(img)
      ret = line_fit(img)
      left_fit = ret['left_fit']
      right_fit = ret['right_fit']
      bottom_y = img.shape[0] - 1
      bottom_x_left = left_fit[0]*(bottom_y**2) + left_fit[1]*bottom_y + left_fit[2]
      bottom_x_right = right_fit[0]*(bottom_y**2) + right_fit[1]*bottom_y + right_fit[2]
      vehicle_offset = img.shape[1]/2 - (bottom_x_left + bottom_x_right)/2
      xm_per_pix = 3.7/680 # meters per pixel in x dimension
      vehicle_offset = vehicle_offset*xm_per_pix
      self.pub.publish(vehicle_offset) # cross track error
      #label_str = 'Vehicle offset from lane center: %.3f m' % self.vehicle_offset
      #img = cv2.putText(img, label_str, (30,70), 0, 1, (255,0,0), 2, cv2.LINE_AA)
    except CvBridgeError as e:
      print(e)

    cv2.imshow("Image window", np.float64(img))
    count += 1
    k = cv2.waitKey(1)
    if k == 113: #q
        cv2.imwrite("saves/"+str(count)+"_new.png", img)
    if k == 27: #esc
        cv2.destroyAllWindows()

def main():
  rospy.init_node('lane_tracker', anonymous=True)
  ic = image_offset()
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
