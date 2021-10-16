#!/usr/bin/env python

from rospy.timer import Rate
from std_msgs.msg import Float32
from sensor_msgs.msg import LaserScan, Imu
from geometry_msgs.msg import Quaternion
import rospy
import time

rospy.init_node("stand_controller")
data_pub_1 = rospy.Publisher("/stand1/command/", Float32, queue_size=1)
data_pub_2 = rospy.Publisher("/stand2/command/", Float32, queue_size=1)

if __name__ == "__main__":

    r = rospy.Rate(
        0.5
    )  # specify rate in Hz based upon your desired PID sampling time, i.e. if desired sample time is 33ms specify rate as 30Hz
    while not rospy.is_shutdown():

        try:
            cmd1=0.0
            cmd2=0.0
            data_pub_1.publish(cmd1)
            data_pub_2.publish(cmd2)
            time.sleep(3)
            print("0 pub")
            cmd1=-0.1
            cmd2=0.1
            data_pub_1.publish(cmd1)
            data_pub_2.publish(cmd2)
            time.sleep(3)
            print("1 pub")
            cmd1= 0.0
            cmd2= 0.0
            data_pub_1.publish(cmd1)
            data_pub_2.publish(cmd2)
            print("done pub")
            
            break
        except rospy.exceptions.ROSTimeMovedBackwardsException:
            pass
