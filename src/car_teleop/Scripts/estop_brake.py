#!/usr/bin/env python
from os import system
import RPi.GPIO as GPIO
import rospy
import time
from std_msgs.msg import String
from geometry_msgs.msg import Twist
#from dbw_polaris_msgs import BrakeCmd
from dbw_fca_msgs import BrakeCmd

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def stopper():
    state=rospy.Publisher("switchState",String, queue_size=10)
    brake=rospy.Publisher("/vehicle/brake_cmd", Twist, queue_size=10)
    rospy.init_node("estop_brake",anonymous=True)
    msg=BrakeCmd()
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        input_state=GPIO.input(18)
        if input_state == False:
            print("Stop - Full brake.")
            msg.pedal_cmd = 0.95
            msg.pedal_cmd_type = 2
            msg.enable = 1
            msg.clear = 1
            msg.ignore = 1
            msg.count = 100
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

#rostopic pub -r 10 /vehicle/brake_cmd dbw_polaris_msgs/BrakeCmd "{pedal_cmd_type: 2,pedal_cmd: 0.5,enable: 1,clear: 1,ignore: 1,count: 100}"
