#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#  
#  @authors Christopher.Beck@stud.hshl.de
#  @authors Johannes.Schaefer@stud.hshl.de
#  

#from MbotMQTT import mbot_drive_straight
#from MbotMQTT import mbot_motor_stop
#from carSubscriber import connectMQTT
import Queue
import array
import pickle
from thread import start_new_thread
from carSubscriberLibrary import readIO
from carSubscriberLibrary import connectMQTT
from time import sleep
workArray = []
bufFloat=[]
f = "io_file.txt"
#distance = 50.0
#workArray contents [Red,RedYellow,Yellow,Green,ttns,currentState]


def main():
	#os.system('python carSubscriber.py')
	print "carSubscriber.py should start"
	
	
	print "Main Started here"
	q = Queue.Queue()
	#start carSubscriber.py as shell process here!
	#file must be in same working director
	try:
		print "Testausgabe 0"
		#Im Moment carSubsriber selber aufrufen
		#start_new_thread(connectMQTT,())

		print "Testausgabe 1"
		#thread.start_new_thread(driveAlgorithm, ())

		print "Testausgabe 2"
		start_new_thread(printIO,())
		
	except:
		print "Error: unable to start thread"

	while 1:
		pass

def timeNextGreenDeadline():
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

def driveAlgorithm():
	#Written by Johannes
	#Distance wird fix angenommen
	#Geschwindigkeitsalgorithmus mit korrekten Werten fehlt noch
	print("Drive Algorithm started here")
	#mbot_drive_straight(my_mbot,serial,255,"forward");
	
def printIO():
	while 1:
		io_data = readIO(f)
		print io_data
		sleep(0.01)
	



if __name__ == '__main__':
	main()

