#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#  
#  @authors Christopher.Beck@stud.hshl.de
#  @authors Johannes.Schaefer@stud.hshl.de
#  

import MbotMQTT.py
import carSubscriber.py
import Queue	

#distance = 50.0
#workArray contents [Red,RedYellow,Yellow,Green,ttns,currentState]

def timeNextGreenDeadline():
	#Function returns a float with time in seconds till the next Green-Phase ends
	if 	workArray[5] == "Green":
		return 0 

	if workArray[5] == "Red":
		#return ((timeRed - ttns) + timeRedYellow)
		return (workArray[0] - workArray[4] +workArray[1])

	if workArray[5] == "Yellow":
		#return ((timeYellow -ttns) + timeRed + timeRedYellow)
		return workArray[2] - workArray[4] + workArray[0] + workArray[1])
		
	if workArray[5] == "Red-Yellow":
		#return ttns
		return workArray[4]
	else:
		return "Time till next Green Deadline can not be calculated"

def driveAlgorithm():
	#Written by Johannes
	#Distance wird fix angenommen
	@TODO
	#Geschwindigkeitsalgorithmus mit korrekten Werten fehlt noch

	if(timeNextGreenDeadline()) == "Time till next Green Deadline can not be calculated:
		#Security Break if no correct Deadline can be calculated
		mbot_motor_stop
		break
		
    elif(timeNextGreenDeadline()) == 0:
		mbot_drive_straight(my_mbot,serial,255,"forward")
	
	elif(timeNextGreenDeadline()) < distance/mbot_speed:
		mbot_motor_stop
	
	elif(timeNextGreenDeadline()) > distance/mbot_speed:
		mbot_speed = distance/timeNextGreenDeadline
		mbot_drive_straight(my_mbot,serial,mbot_speed,"forward")

def main():
	#start carSubscriber.py as shell process here!
	#file must be in same working director
	os.system('python carSubscriber.py')

	#while noInterupt in Array here einsetzen?
	io = open("io_file.txt","wb")
	workArray = io.read([count])
	io.close()

	driveAlgorithm()


if __name__ == '__main__':
	main()

