#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped

import serial
import random
import sys
import time
from datetime import datetime
# initialise random 2 digit integer
random.seed(datetime.now())
ni=random.randint(10,99)
#Important variables
timeout = 0.150
gcs=[['Node Identifier',2,ni],['Set_X',4,-1],['Set_Y',4,-1],['Set_Z',4,-1]]
drone=[['Node Identifier',2,ni],['Velocity_X',4,69],['Velocity_Y',4,4.20]]
ser = serial.Serial('/dev/ttyACM0','19200')
gcs_data=[]
processed_data1=[['Node Identifier',2,ni],['Set_X',4,-1],['Set_Y',4,-1],['Set_Z',4,-1]]



def print_data(data,info,num_drones):
    processed_data=[]
    line_end=0
    for i in range(int(num_drones)):
        print(str(i+1))
        
        temp_list=[]
        for j in range(len(info)):
            
            print(info[j][0]+" : "+data[line_end:line_end+info[j][1]])
            temp_list.append(data[i][line_end:line_end+info[j][1]])
            processed_data1[j][2]= float(data[line_end:line_end+info[j][1]])
            line_end = line_end + info[j][1]
        processed_data.append(temp_list)
    return processed_data


def size(info):
    sum = 0
    for i in range(len(info)):
        sum = sum + int(info[i][1])
    return sum
def num2str(a,b):
    length = len(str(round(a)))+1
    op ='"%.'+str(b-length)+'f"'
    
    return (op % a)[1:-1]
def gather(drone):
    string=''
    string=string+str(drone[0][2])
    print("Droney",drone)
    for i in range(1,len(drone)):
        string=string+num2str(drone[i][2],drone[i][1])
    return string


pub = rospy.Publisher('gefucc', PoseStamped, queue_size=10)    #ros pub
rospy.init_node('talker', anonymous=True)
setp_msg = PoseStamped()
rate = rospy.Rate(10) # 10hz

cont = True
while (cont):
    send_data = gather(drone)
    time.sleep(0.02)
    print(send_data)
    print((send_data.encode()))
    ser.write(send_data.encode())    # write a string
    a = ser.read(int(4))
    print(a)
    num_drones=int(round(float((a).decode())))
    print("Num Drones :"+str(num_drones))
    print(num_drones*int(size(gcs)))
    gcs_table = ser.read(num_drones*int(size(gcs)))
    print("ha")
    decoded_data = gcs_table.decode()
    print_data(decoded_data,gcs,num_drones)
    
    setp_msg.pose.position.x= processed_data1[1][2]   #ros pub
    setp_msg.pose.position.y= processed_data1[2][2]
    setp_msg.pose.position.z= processed_data1[3][2]

    pub.publish(setp_msg)

    if(gcs_table== b''):
        cont = False


ser.close()
