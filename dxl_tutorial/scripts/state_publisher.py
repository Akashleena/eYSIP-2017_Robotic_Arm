#!/usr/bin/env python

import rospy
from sensor_msgs.msg import JointState
from dynamixel_msgs.msg import MotorState
from dynamixel_msgs.msg import MotorStateList
from math import pi
import time

rospy.init_node('State_Publisher')

joints = ["shoulder_pan_joint","shoulder_pitch_joint","shoulder_yaw_joint","elbow_pitch_joint","elbow_roll_joint","wrist_pitch_joint"]
offset = [666,512,512,375,512,682]

def callback(msg):
	joint_states = JointState()

	#print msg	
	joint_states.header.stamp = rospy.Time.now()

	for x in msg.motor_states:
		joint_states.name.append(joints[x.id-1])

		if(not (x.id==2 or x.id==4)):
			joint_states.position.append((x.position-offset[x.id-1])*(300.0/1023)*(pi/180))
		else:
			joint_states.position.append((offset[x.id-1]-x.position)*(300.0/1023)*(pi/180))
		#joint_states.velocity.append(x.velocity)
	
	pub.publish(joint_states)

sub = rospy.Subscriber('/motor_states/dxl_port',MotorStateList,callback)
pub = rospy.Publisher('/robotic_arm/joint_states',JointState,queue_size=10)

rospy.spin()