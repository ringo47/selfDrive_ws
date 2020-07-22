#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
from os import system
from dataspeed_ulc_msgs.msg import UlcCmd

def callback(data):
    ctError = data.data
    print("Cross Track Error: ",ctError)
    kp = -0.1
    car.yaw_command = kp*ctError
    car.linear_velocity = 0.1
    pub_car.publish(car)
    print("Publishing velocity: ", car.linear_velocity,"m/s and", "yaw :",car.yaw_command)
    
    
def main():
    global car, pub_car
    #system("rostopic pub -r 10 /vehicle/brake_cmd dbw_fca_msgs/BrakeCmd ""{pedal_cmd_type: 2edal_cmd: 0.5,enable: 1,clear: 1,ignore: 1,count: 100}"")
    rospy.sleep(5)
    system("rosnode kill /path_following")
    car = UlcCmd()
    car.clear = False
    car.enable_pedals = True
    car.enable_steering = True
    car.linear_velocity = 0
    car.shift_from_park = False
    car.enable_shifting = False
    car.lateral_accel = 0.5
    car.linear_accel = 0.1
    car.linear_decel = 5.0
    car.yaw_command = 0.00
    car.angular_accel = 0.0
    car.steering_mode=0
    rospy.init_node('lane_follower_pid', anonymous=True)
    pub_car = rospy.Publisher('/vehicle/ulc_cmd', UlcCmd,queue_size=10)
    pub_car.publish(car)
    rospy.Subscriber("laneOffset", Float32, callback)
    system("rosnode kill /path_following")
    

    rospy.spin()

if __name__ == '__main__':
    main()