#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#  
#  Copyright 2017  <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

#import MbotMQTT
from MbotMQTT import mbot_drive_straight
from MbotMQTT import mbot_motor_stop
from MbotMQTT import Mbot_start
#from carSubscriberLibrary import readIO
import time
workArray=[ 10.,1.,3.,10.,5.,"Green"]

start_distance = 50.0
start_speed = 155
start_speedsi = (0.42/255)*155
max_speed = 255
min_speed = 55
min_speedsi = (0.42/255)*55

current_milli_time = lambda: int(round(time.time() * 1000))


def main():
	driveAlgorithm()

	
def driveAlgorithm():
	t0 = current_milli_time()
   #while Mbot_start() == 1:
	while 1:
		if timeNextGreenStart == "error":
			break
		else:
			mbot_drive_straight(my_mbot,serial,start_speed,"foreward")		    
			tta = start_distance/start_speedsi
		
			# wenn die Grünphase erreicht werden kann, dann behalte Geschwindigkeit
			if timeNextGreenStart()< tta and workArray[4] > tta:
				mbot_drive_straight(my_mbot,serial,start_speed,"foreward")
		
			#Mbot würde vor oder nach der Grünphase ankommen
			elif timeNextGreenStart() > tta or workarray[4] < tta:
			
			#Mbot muss an der Ampel stoppen
				if timeNextGreenStart() > start_distance/min_speed:
					slowdown()
					tnow = current_milli_time()
					distance = ((start_speedsi+min_speedsi)/2)*(tnow-t0)
					if distance >= start_distance:
						mbot_motor_stop()
					
			#Geschwindigkeit wird angepasst, sodass Mbot bei grün ankommt		
			else:
				new_speed = distance/timeNextGreenStart()
				mbot_drive_straight(my_mbot,serial,new_speed,"foreward")
		

def timeNextGreenStart():
	#Function returns a float with time in seconds till the next Green-Phase ends
	if 	workArray[5] == "Green":
		return 0 
		print("--------------------------------------------------Green received in main.py")

	if workArray[5] == "Red":
		#return ((timeRed - ttns) + timeRedYellow)
		return (workArray[0] - workArray[4] +workArray[1])
		print("--------------------------------------------------Red received in main.py")

	if workArray[5] == "Yellow":
		#return ((timeYellow -ttns) + timeRed + timeRedYellow)
		return (workArray[2] - workArray[4] + workArray[0] + workArray[1])
		print("--------------------------------------------------Yellow received in main.py")

		
	if workArray[5] == "Red-Yellow":
		#return ttns
		return workArray[4]
		print("--------------------------------------------------Red-Yellow received in main.py")
	else:
		return "Time till next Green Deadline can not be calculated"
def slowdown():
	for new_speed in range(start_speed,min_speed):
		mbot_drive_straight(my_mbot,serial,new_speed,"foreward")
		new_speed= newspeed-1
		sleep(0.2)
	 
	


if __name__ == '__main__':
	main()

