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
    nConformations = 0 #number of times the body part has been identified (used to ramp speed up and down)
    transLast = 0
    lastLinear = 0
    lastAngular = 0
    while not rospy.is_shutdown():
        try:
            (trans,rot) = listener.lookupTransform('/openni_depth_frame', '/torso_1',  rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
 	    cmd = geometry_msgs.msg.Twist()
            cmd.linear.x = 0
            cmd.angular.z = 0
            turtle_vel.publish(cmd)
            continue
	
	if transLast == trans:
            cmd = geometry_msgs.msg.Twist()
            cmd.linear.x = lastLinear / 1.4
            cmd.angular.z = 0
            turtle_vel.publish(cmd)
	    lastLinear = lastLinear / 1.4
            continue

        angularGoal= 4 * math.atan2(trans[1], trans[0])
	dist = math.sqrt(trans[0] ** 2 + trans[1] ** 2)
	distFromDesired = dist - 2
	linearGoal = .5 * distFromDesired

	#bound linear and angular goals
	if linearGoal > .3:
           linearGoal = .3

	if linearGoal < -.3:
	   linearGoal = -.3	    

	if angularGoal > .5:
	   angularGoal = .5

	if angularGoal < -.5:
	   angularGoal = -.5

	
	#ramp up angular and linear speeds
	if lastLinear < linearGoal:
	   lastLinear += .02

	else:
	   lastLinear -= .02

	if lastAngular < angularGoal:
	   lastAngular += .1

	else:
	   lastAngular += -.1

        #send message
	#rospy.loginfo("linearGoal = %f, angularGoal = %f,  dist = %f", linearGoal, angularGoal, dist)
	rospy.loginfo("trans[1] = %f, trans[0] = %f", trans[1], trans[0])        
	cmd = geometry_msgs.msg.Twist()
        cmd.linear.x = lastLinear
        cmd.angular.z = lastAngular
        turtle_vel.publish(cmd)
	transLast = trans
        rate.sleep()
