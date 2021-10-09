#!/usr/bin/env python

from std_msgs.msg import Float32
from sensor_msgs.msg import LaserScan, Imu
from geometry_msgs.msg import Quaternion
import rospy
import tf


class sbb:
    def __init__(self):

        rospy.init_node("controller")

        self.sbb_orientation_quaternion = [0.0, 0.0, 0.0, 0.0]
        self.sbb_orientation_euler = [0.0, 0.0, 0.0]

        self.sample_rate = 50.0  # in Hz

        self.w = 0.0
        self.curr_angle = 0.0
        self.prev_angle = 0.0
        self.kp = 0
        self.ki = 0
        self.reset=0
        self.angle_sum=0

        self.data_cmd = Float32()
        self.data_cmd.data = 0.0

        self.data_pub = rospy.Publisher("/flywheel/command", Float32, queue_size=1)

        rospy.Subscriber("/sbb/imu", Imu, self.imu_callback)

    def imu_callback(self, msg):

        self.sbb_orientation_quaternion[0] = msg.orientation.x
        self.sbb_orientation_quaternion[1] = msg.orientation.y
        self.sbb_orientation_quaternion[2] = msg.orientation.z
        self.sbb_orientation_quaternion[3] = msg.orientation.w

    def pid(self, Kp,Ki,Kd):
        (
            self.sbb_orientation_euler[1],
            self.sbb_orientation_euler[0],
            self.sbb_orientation_euler[2],
        ) = tf.transformations.euler_from_quaternion(
            [
                self.sbb_orientation_quaternion[0],
                self.sbb_orientation_quaternion[1],
                self.sbb_orientation_quaternion[2],
                self.sbb_orientation_quaternion[3],
            ]
        )
        self.kp=Kp
        self.ki=Ki
        self.kd=Kd

        # print(self.sbb_orientation_euler[1])
        self.curr_angle = self.sbb_orientation_euler[1]

        self.angle_sum+=self.curr_angle
        self.angle_diff=self.curr_angle-self.prev_angle

        if self.curr_angle > 0:

            if self.reset == 0:
                self.w = 0

            self.w = self.kp * self.curr_angle + self.ki*self.angle_sum + self.kd*self.angle_diff
            self.data_cmd.data = self.w
            self.reset = 1

        if self.curr_angle < 0:
            if self.reset == 1:
                self.w = 0
            self.w = self.kp * self.curr_angle + self.ki*self.angle_sum + self.kd*self.angle_diff
            self.data_cmd.data = self.w
            self.reset = 0

        self.prev_angle = self.curr_angle
        
        # print(self.data_cmd.data)

        self.data_pub.publish(self.data_cmd)


if __name__ == "__main__":

    sbb = sbb()
    r = rospy.Rate(
        50
    )  # specify rate in Hz based upon your desired PID sampling time, i.e. if desired sample time is 33ms specify rate as 30Hz
    while not rospy.is_shutdown():

        try:
            sbb.pid(35,1.7,1) # PI Controller
            r.sleep()
        except rospy.exceptions.ROSTimeMovedBackwardsException:
            pass
