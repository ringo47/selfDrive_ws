#!/usr/bin/env python3
import numpy
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
    pub_car = rospy.Publisher('/vehicle/ulc_cmd', UlcCmd,queue_size=10)
    c.clear = False
    c.enable_pedals = True
    c.enable_steering = True
    c.linear_velocity = 0.5
    c.shift_from_park = False
    c.enable_shifting = False
    c.lateral_accel = 0.5
    c.linear_accel = 0.1
    c.linear_decel = 5.0
    c.yaw_command = 0.00
    c.angular_accel = 0.0
    velocityStep = 0.5
    deceleration = 1 #m/s^2
    yawStep = 0.1
    yaw_deceleration = 1
    c.steering_mode=0
    t=rospy.get_time()
    with KeyPoller() as keyPoller:
        while not rospy.is_shutdown():
            time.sleep(0.01)
            k=keyPoller.poll()
            if k=='w':
                c.linear_velocity += velocityStep
                pub_car.publish(c)
                rospy.loginfo(str(k)) 
                pub.publish(k)
                continue
            if k=='s':
                c.linear_velocity -= velocityStep
                pub_car.publish(c)
                rospy.loginfo(str(k)) 
                pub.publish(k)
                continue
            if k=='d':
                c.yaw_command -= yawStep
                pub_car.publish(c)
                rospy.loginfo(str(k)) 
                pub.publish(k)
                continue
            if k=='a':
                c.yaw_command += yawStep
                rospy.loginfo(str(k)) 
                pub.publish(k)
                continue

            elapsed_time = rospy.get_time() - t
            c.linear_velocity -= deceleration*numpy.sign(c.linear_velocity)*elapsed_time
            c.yaw_command -= yaw_deceleration*numpy.sign(c.yaw_command)*elapsed_time
            pub_car.publish(c)
            rospy.loginfo(str(k)) 
            pub.publish(k)
            t=rospy.get_time()
            
            

if __name__=='__main__':
    try:
        controller()
    except rospy.ROSInterruptException:
        pass
