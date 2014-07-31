#!/usr/bin/env python

#Author: Andrew Cunningham

import rospy
import math
import tf
import geometry_msgs.msg

#initialize velocities to 0
global currentAngularV
global currentLinearV
currentAngularV = 0
currentLinearV = 0

global lastX
lastX = 0

def callback(data):
    global currentLinearV
    global currentAngularV
    global turtle_vel
    global lastX

    #calculate angular displacement
    angularDisplacement = math.atan2(data.x, data.y)

    #calculate distance to person
    dist = math.sqrt(data.x ** 2 + data.y ** 2)
    distFromDesired = dist - .35 #.4 is set according to user preference
 
    #calculate velocity goals
    linearGoal = 3 * distFromDesired
    angularGoal = 2 * angularDisplacement
	
    if data.x == lastX or (data.y < 0.01 and data.x < 0.01):
	linearGoal = 0
	angularGoal = 0

    #used to make sure that repeat CoM's aren't used to drive the robot
    lastX = data.x
    #bound linear and angular goals
    if linearGoal > .7:
        linearGoal = .7

    if linearGoal < -.5:
        linearGoal = -.5

    if angularGoal > .7:
        angularGoal = .7
        linearGoal = 0

    if angularGoal < -.7:
        angularGoal = -.7
        linearGoal = 0

    #take current velocities into account to allow for smooth transistions
    if currentLinearV < linearGoal:
        currentLinearV += .02

    else:
        currentLinearV -= .02

    if currentAngularV < angularGoal:
        currentAngularV += .1

    else:
        currentAngularV -= .05

    cmd = geometry_msgs.msg.Twist()
    cmd.linear.x = currentLinearV
    cmd.angular.z = currentAngularV
    turtle_vel.publish(cmd)


def listener():
    rospy.init_node('personFollower', anonymous=True)
    global turtle_vel
    turtle_vel = rospy.Publisher('/cmd_vel_mux/input/teleop', geometry_msgs.msg.Twist)
    rospy.Subscriber("personCoM", geometry_msgs.msg.Pose2D, callback)


    rospy.spin()
        
if __name__ == '__main__':
    listener()
