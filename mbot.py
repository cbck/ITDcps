"""
This script is the Communication Interface for the Mbot Platform. It generates a Message Buffer witch is send over the serial port (ttyAMA0) 
to the Mbot. This script also recive serial messages from the Mbot and returns it.
It is not fully compatible with all fuctions of the Mbot because only these functions are required for the Project. The other functions 
might be implemented later ;)

to run these script on a RaspberryPi 3 the following librarys are required
	python-serial 		(sudo apt-get install python-serial)
	time

Author: Daniel Muenstermann; Email: dainel.muenstermann@stud.hshl.de
"""

import serial
import time
from collections import namedtuple

#functions to communicate with the Mbot platform

#Stops the Mbot
def mbot_motor_stop(serial):
	mbot_message(serial,"set","motor","left","",[0,0])
	mbot_message(serial,"set","motor","right","",[0,0])

#Let the Mbot drive forward or backward #drives both Motors exactly synchron
def mbot_drive_straight(serial,speed,direction):
	#right motor
	#if speed  0:
	#	sp = 
	
	
	#left motor
	#[0,255] => full forward
	#[255,0] => full Backward
	if direction == "forward":
		mbot_message(serial,"set","motor","left","",[255-speed, 255])
		mbot_message(serial,"set","motor","right","",[speed, 0])
		
		
	elif direction == "backward":
		mbot_message(serial,"set","motor","left","",[speed,0])
		mbot_message(serial,"set","motor","right","",[255-speed,255])

#Drives only the left Motor forward or backward
def left_Motor(serial, speed, direction):
	#drives the left Motor
	mbot_message(serial,"set","motor","left","",[255, 30])

#Drives only the right Motor forward or backward
def right_motor(serial, speed, direction):
	#drives the right Motor
	mbot_message(serial,"set","motor","right","",[255, 30])
	
"""
#Triggers the Mbot to send the Motor Encoder Data, recive it and return it
def get_encoder_data (mbot, serial):
	#trigger the Mbot to send the Encoder Data
"""
#Build the message for the communication protokoll
def mbot_message(serial, action, device, port, slot, data):

	#Get action instruction and set it to the Value of the protokoll
	if action == "get":
		set_action = int("01", 16)
	elif action == "set":
		set_action = int("02", 16)
	elif action == "reset":
		set_action = int("04", 16)
	else:
		set_action = int("05", 16)

	#Get Device information and set it to the Value of the protokoll
	if device == "motor":
		set_device = int("0A", 16)
	elif device == "servo":
		set_device = int("0B", 16)
	elif device == "encoder":
		set_device = int("0C", 16)
	elif device == "ultrasonic":
		set_device = int("01", 16)

	#Get Port information and set it to the Value of the protokoll
	if port == "left":
		set_port = int("09", 16)
	elif port == "right":
		set_port = int("0A", 16)
	elif port == "arm":
		set_port = int("0B", 16)

	#Get Slot information and set it to the Value of the protokoll
	#The Slot data is required for reading sensor data
	#if slot == "slot":
	set_slot = slot
	set_data = data


	msg = [ int("FF", 16), int("55", 16),		#Header
			int("00", 16),						#length
			int("00", 16)]						#IDX => always 0

	#If there is no entry for the action, than dont write it to the message
	if action != "":
		msg.append (set_action)					#action "01" => GET; "02" => RUN; "04" => RESET; "05" => START

	#If there is no entry for the device, than dont write it to the message
	if device != "":
		msg.append (set_device)					#device "0A" => MOTOR; "0B" => SERVO; "0C" => ENCODER

	#If there is no entry for the port, than dont write it to the message
	if port != "":
		msg.append (set_port)					#port 	"09" => left Motor; "0A" => right Motor 

	#If there is no entry for the slot, than dont write it to the message
	if slot != "":
		msg.append (set_slot)					#slot 	

	#if there are more than zero entrys for the data, write them to the msg
	if len(set_data) >= 0:
		for data_byte in range(0, len(set_data)):
			msg.append (set_data[data_byte])	#data 	"Speed" + "dir"
	
	#After the Message is putted together, calculate the length replace it
	msg[2] = len(msg)-3

	#At this Point the message is ready to be send
	print (msg)
	serial.write(msg)

#Global Variables
wheel_diameter_cm = 10
encoder_counts_per_turn = 360		
wheel_circumference = 31.4159		#pi * wheel_diameter_cm
wheel_distance = 23.6				#distance between the left and right wheel
tics_per_cm = 11.4591				#encoder_counts_per_turn / wheel_circumference
acceleration = 1					#default Acceleration
mode = 0							#Mode 0 => 0 Full Reverse; 128 Stop Motor; 255 = Full Forward
speedregulation = 1					#1 = on ; 0 = off

#																								INIT							length			idx				action			device			port				slot						data
#my_mbot =mbot(wheel_distance, tics_per_cm, encoder_counts_per_turn, wheel_diameter_cm, [int("FF", 16), int("55", 16)],[int("06", 16)],[int("00", 16)],[int("02", 16)],[int("0A", 16)],[int("09", 16)],[int("FF",16), int("FF", 16)],[int("00", 16)])

#initialise the Serial PL011 Serial 
serial = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=3.0)

#init_robot(my_robot, serial, acceleration, mode, speedregulation)

"""
#Testmessage
print "jetzt kommt der Ultraschalltest"
mbot_message(my_mbot, serial, "get", "ultrasonic", "",3, "")

#print "jetzt kommt die message"
serial.flush()
#mbot_message(my_mbot,serial,"get","encoder","left","","")
read_data = serial.read(1)

print "jetzt kommt read data"
print read_data

#mbot_message(my_mbot,serial,"set","motor","left","",[128,0])

#mbot_message(my_mbot,serial,"set","motor","right","",[0,0])

#Attention, The Arm has no Endstops
#mbot_message(my_mbot,serial,"set","motor","arm","",[255,0])
"""
"""
mbot_message(my_mbot,serial,"get","encoder","left","","")
read_data = serial.read(8)
print read_data
"""

"""
speed = 255
mbot_drive_straight(my_mbot,serial,speed,"forward")
time.sleep(2)
speed = 128
mbot_drive_straight(my_mbot,serial,speed,"forward")
time.sleep(2)
speed = 60
mbot_drive_straight(my_mbot,serial,speed,"forward")
time.sleep(2)
speed = 0
mbot_drive_straight(my_mbot,serial,speed,"forward")
time.sleep(2)
speed = 60
mbot_drive_straight(my_mbot,serial,speed,"backward")

mbot_motor_stop(my_mbot,serial)
"""

"""
for x in range (0,255):
	#mbot_message(my_mbot,serial,"set","motor","right","",[x,0])
	mbot_drive_straight(serial,x,"forward")
	time.sleep(0.01)
time.sleep(3)
mbot_motor_stop(serial)
"""

"""
msg = [int("FF", 16)]
#port.write(msg)
print (msg)

msg = [int("55", 16)]
#port.write(msg)
print (msg)

msg = [int("06", 16)]
#port.write(msg)
print (msg)

msg = [int("00", 16)]
#port.write(msg)
print (msg)

msg = [int("02", 16)]
#port.write(msg)
print (msg)

msg = [int("0A", 16)]
#port.write(msg)
print (msg)

msg = [int("09", 16)]
#port.write(msg)
print (msg)

msg = [int("FF", 16)]
#port.write(msg)
print (msg)

msg = [int("FF", 16)]
#port.write(msg)
print (msg)

msg = [int("00", 16)]
#port.write(msg)
print (msg)
"""


"""
#Testumgebung 
msg = [my_robot.MD25_SET_SPEED1[0], my_robot.MD25_SET_SPEED1[1],200]
port.write(msg)
msg = [my_robot.MD25_SET_SPEED2 [0], my_robot.MD25_SET_SPEED2 [1], 200]
port.write(msg)

time.sleep(2)

msg = [my_robot.MD25_SET_SPEED1[0], my_robot.MD25_SET_SPEED1[1],128]
port.write(msg)
msg = [my_robot.MD25_SET_SPEED2 [0], my_robot.MD25_SET_SPEED2 [1], 128]
port.write(msg)
"""
