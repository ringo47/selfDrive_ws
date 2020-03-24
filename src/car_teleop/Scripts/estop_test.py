#!/usr/bin/env python
from os import system
import RPi.GPIO as GPIO
import rospy
import time
from std_msgs.msg import String
from geometry_msgs.msg import Twist

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def stopper():
    state=rospy.Publisher("switchState",String, queue_size=10)
    brake=rospy.Publisher("/vehicle/cmd_vel", Twist, queue_size=10)
    rospy.init_node("estop",anonymous=True)
    msg=Twist()
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        input_state=GPIO.input(18)
        if input_state == False:
            print("Stop")
            msg.linear.x=0.0
            msg.linear.y=0.0
            msg.linear.z=0.0
            msg.angular.x=0.0
            msg.angular.y=0.0
            msg.angular.z=0.0
            time.sleep(0.1)
            brake.publish(msg)
        state.publish(str(input_state))
        rospy.loginfo(str(input_state))
        rate.sleep()


if __name__=='__main__':
    try:
        stopper()
        GPIO.cleanup()
        print("GPIO Cleanup")
    except rospy.ROSInterruptException:
        pass
