#!/usr/bin/env python3
# license removed for brevity
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped

x1 = 10
y1 = 20
z1 = 30
def talker():
    global x1,y1,z1
    pub = rospy.Publisher('gfucc', PoseStamped, queue_size=10 )
    rospy.init_node('talker', anonymous=True)
    setp_msg = PoseStamped()
    rate = rospy.Rate(5) # 10hz

    while not rospy.is_shutdown():
        x1=x1+1
        y1+=2
        z1+=3
        setp_msg.pose.position.x = x1    #ros pub
        setp_msg.pose.position.y = y1
        setp_msg.pose.position.z = z1

        pub.publish(setp_msg)
        rate.sleep()
   
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass