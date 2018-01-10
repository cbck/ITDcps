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
#import carSubscriberLibrary
from carSubscriberLibrary import connectMQTT
from carSubscriberLibrary import on_message
from carSubscriberLibrary import driveWithQueue
from carSubscriberLibrary import testQueue
import Queue
import array
import pickle
#from thread import start_new_thread
import threading
#from carSubscriberLibrary import readIO
#from carSubscriberLibrary import connectMQTT
from time import sleep
Broker="172.31.12.122"
workArray = []
bufFloat=[]
f = "io_file.txt"
#distance = 50.0
#workArray contents [Red,RedYellow,Yellow,Green,ttns,currentState]


def main():

	#os.system('python carSubscriber.py')
	print "carSubscriber.py should start"
	mqttConnection = connectMQTT(Broker)
	mqttConnection.start()
	
	print "Main Started here"
	#q = Queue.Queue()
	driveWithQueue()
	testQueue()

	'''
	try:
		print "Testausgabe 0"
		#Im Moment carSubsriber selber aufrufen
		#start_new_thread(connectMQTT,(self,Broker))
			
		print "Testausgabe 1"
		#thread.start_new_thread(driveAlgorithm, ())

		print "Testausgabe 2"
		#start_new_thread(printIO,())
		
	except:
		print "Error: unable to start thread"

	while 1:
		pass
	'''


'''
def driveAlgorithm():
	#Written by Johannes
	#Distance wird fix angenommen
	print("Drive Algorithm started here")
	
    if timeNextGreenState == "error":
		break
	
	elif CS == "Green":
		#workArray[4] ist TTNS
	  if workArray[4] > distance/mbot_speed: 
		 mbot_drive_straight(my_mbot,serial,mbot_speed,"foreward")
		  	
	elif timeNextGreenState > distance/mbot_speed:
		if 
		mbot_speed = distance/timeNextGreenDeadline
		mbot_drive_straight(my_mbot,serial,mbot_speed,"foreward")		
'''
'''	
def printIO():
	while 1:
		io_data = readIO(f)
		print io_data
		sleep(0.01)
'''



if __name__ == '__main__':
	main()

