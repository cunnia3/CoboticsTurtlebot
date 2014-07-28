#!/usr/bin/env python  
import roslib
import rospy
import math
import tf
import geometry_msgs.msg

if __name__ == '__main__':
    rospy.init_node('tf_personFollower')

    listener = tf.TransformListener()

    turtle_vel = rospy.Publisher('/cmd_vel_mux/input/teleop', geometry_msgs.msg.Twist)

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
	rospy.loginfo("test")
        try:
            (trans,rot) = listener.lookupTransform('/torso', '/openni_depth_frame', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        angular = 4 * math.atan2(trans[1], trans[0])
        linear = 0.5 * math.sqrt(trans[0] ** 2 + trans[1] ** 2)
        cmd = geometry_msgs.msg.Twist()
        cmd.linear.x = linear
        cmd.angular.z = angular
        turtle_vel.publish(cmd)

        rate.sleep()





