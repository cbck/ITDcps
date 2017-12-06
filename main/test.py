"""
This is a small Test programm to verify that the mbot_drive_straight and the mbot_motor_stop function
is callable from an other file. 
Therefore its required that the serial is implemented in the main loop. 

"""

from mbot import mbot_drive_straight
from mbot import mbot_motor_stop
import time 
import serial

#Init the serial 
serial = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=3.0)

#get mqtt messages

#clock sync ??? 



# drive forward 

# get SPI interupts 

# calculate speed

# compare with traffic light time slot and calculate new speed



direction = "backward"



for x in range (1,255):
	
	mbot_drive_straight(serial,x,direction)

	time.sleep(0.003)

time.sleep(2)



mbot_motor_stop(serial)
