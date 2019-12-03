#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped


 
def callback(data):
    print("thru")
    rospy.loginfo(rospy.get_caller_id() + "Setpoint X %s", data.pose.position.x)
    rospy.loginfo(rospy.get_caller_id() + "Setpoint Y %s", data.pose.position.y)
    rospy.loginfo(rospy.get_caller_id() + "Setpoint Z %s", data.pose.position.z)

    
    #print("we try get {}".format(data.data))
def listener():
 
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("gefucc", PoseStamped, callback)
    
    print("I love u")
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
 
if __name__ == '__main__':
    listener()
