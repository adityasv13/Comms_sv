#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped

import serial
import time
import sys

ni=0
timeout = 0.200
# gcs=[['Node Identifier',2,ni],['Set_X',4,3],['Set_Y',4,2]]
# drone=[['Node Identifier',2,ni],['Velocity_X',4,-1],['Velocity_Y',4,-1]]

gcs=[['Node Identifier',2,ni],['Set_X',4,3],['Set_Y',4,4],['Set_Z',4,5]]
drone=[['Node Identifier',2,ni],['Velocity_X',4,-1],['Velocity_Y',4,-1]]
ser = serial.Serial('/dev/ttyACM1','19200',timeout=float(0.01))
drone_data=[]

def callback(data):
    
    
    gcs[1][2]=data.pose.position.x
    gcs[2][2]=data.pose.position.y
    gcs[3][2]=data.pose.position.z
    #print("we try get {}".format(data.data))

rospy.init_node('listener', anonymous=True)

rospy.Subscriber("gfucc", PoseStamped, callback)


def size(info):
    sum = 0
    for i in range(len(info)):
        sum = sum + int(info[i][1])
    return sum

def print_data(data,info):
    processed_data=[]
    for i in range(len(data)):
        line_end=0
        temp_list=[]
        for j in range(len(info)):
            print(info[j][0]+" : "+str(data[i][line_end:(line_end+info[j][1])]))
            temp_list.append(data[i][line_end:line_end+info[j][1]])
            line_end = line_end + info[j][1]
        processed_data.append(temp_list)
    return processed_data,len(data)

def num2str(a,b):
    length = len(str(round(a)))+1
    op ='"%.'+str(b-length)+'f"'
    return (op % a)[1:-1]

def gather(data,gcs):
    string=''
    for i in range(len(data)):
        print("data",data)
        string=string+data[i][0]
        for i in range(1,len(gcs)):
            string = string+num2str(gcs[i][2],gcs[i][1]) #1gcs to data
        print("stringsend  " , string, "  number" , i)
    return string
def process(data,size):
    processed_list=[]
    joined=''.join(data)
    if(len(joined)%size!=0):
        print("Scammed Data")
        return 0
    processed_list = [(joined[i:i+size]) for i in range(0, len(joined), size)]
    return processed_list

k=0
while True:
    k = k+1
    # print(k)
    start = time.time()
    end = time.time()
    size_recieve = size(drone)
    drone_data=[]
    while(end-start<timeout):
        data = ser.read(int(size_recieve))
        end=time.time()
        if(data != b''):
            print(data.decode())
            drone_data.append(data.decode())
    if(drone_data!=[]):
        print(drone_data)
        drone_data = process(drone_data,size_recieve)
        print(drone_data)
        processed_data,num_drones = print_data(drone_data,drone)
        print(processed_data)
        # Gather Data from Other Nodes
        # writing a Temporary function to initialise random values
        print("Sending Number of Drones :"+str(num2str(num_drones,4)))
        time.sleep(1)
        ser.write(str(num2str(num_drones,4)).encode())
        send_data = gather(processed_data,gcs)
        print("Data to send :")
        print("Send data",send_data)
        print("sizel",num_drones*int(size(gcs)))
        ser.write(send_data.encode())    # write a string
        print("all sent encoded",len(send_data.encode()))
        print("1all sent",len(send_data))

ser.close()             # close port
