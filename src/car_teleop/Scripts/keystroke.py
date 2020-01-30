#!/usr/bin/env python3
from os import system
import rospy
from dataspeed_ulc_msgs.msg import UlcCmd
import getch
from std_msgs.msg import Int8
from timeout_key import KeyPoller
import time

def controller():
    system("rosnode kill /path_following")
    pub = rospy.Publisher('key',Int8,queue_size=10) 
    rospy.init_node('keystroke',anonymous=True)
    c=UlcCmd()
    pub_car=rospy.Publisher('/vehicle/ulc_cmd', UlcCmd,queue_size=10)
    c.clear=False
    c.enable_pedals=True
    c.enable_steering=True
    c.linear_velocity=1.0
    c.shift_from_park=False
    c.enable_shifting=False
    c.lateral_accel=8.0
    c.linear_accel=1.0
    c.linear_decel=0.0
    c.yaw_command=0.03
    c.angular_accel=0.0
    c.steering_mode=0
    with KeyPoller() as keyPoller:
        while not rospy.is_shutdown():
            time.sleep(0.01)
            k=keyPoller.poll()
            if k=='w':
                c.linear_velocity += 0.1
            if k=='s':
                c.linear_velocity -= 0.1
            if k=='d':
                c.yaw_command -= 0.01
            if k=='a':
                c.yaw_command += 0.01
            
            rospy.loginfo(str(k)) 
            pub.publish(k)
            pub_car.publish(c)

if __name__=='__main__':
    try:
        controller()
    except rospy.ROSInterruptException:
        pass
