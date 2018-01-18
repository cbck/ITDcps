#!/usr/bin/env python
# -*- coding: utf-8 -*-
#This main function has the purpose to start two Threads (15.January 2018)
#One Thread is started by the init process of connectMQTT Object

import paho.mqtt.client as mqtt
#import MbotMQTT
from mbot import mbot_drive_straight
from mbot import mbot_motor_stop
#from MbotMQTT import Mbot_start
#from carSubscriberLibrary import readIO
import time
import serial
import threading
import Queue
from threading import Thread

serial = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=3.0)

start_distance = 5.0			#Dummwert in Meter
start_speed = 255				#Integer for motor value 0...255
start_speedsi = (0.42/255)*start_speed	#in meter/seconds
max_speed = 255					#int
min_speed = 55					#int
min_speedsi = (0.42/255)*min_speed
noInterupt = True

#Broker is running via a dedicated windows pc 
#The MQTT.fx ,Broker is used on Windows(@Johannes?)
Broker="172.31.12.122"			
topic_pub="traffiLight/carMessage"

#Global variables for MQTT Transfer
global timeRed 
global timeRedYellow 
global timeGreen
global timeYellow 
global m_start_signal
global workArray
global state
global TTNS
global timestamp 
global iRed 
global iRedYellow 
global iGreen 
global iYellow       
global interupt 
global CS 
global startTopic 
global currentState

#Subscribe Topics all starting with traffiLight/ for
state = "traffiLight/state"             #dummy topic
TTNS = "traffiLight/timeTillNextState"  #refreshed subtopic showing time till change in seconds
timestamp = "traffiLight/timestamp"		#UTC Servertime from Trafficlight !!!Not needed yet"
iRed = "traffiLight/iRed"               #interval for Red in Seconds
iRedYellow = "traffiLight/iRedYellow"   #interval for Red-Yellow in Seconds
iGreen = "traffiLight/iGreen"           #interval for Green in Seconds
iYellow = "traffiLight/iYellow"         #interval for Yellow in Seconds
interupt = "traffiLight/interupt"       #interupt if Bus/RTW comes and other
CS = "traffiLight/currentState"			#current state as string, can be "Green","Red","Red-Yellow" and "Yellow"
startTopic = "traffiLight/start"		#topic to read start signal from for starting mBot from distance
currentState = ""						#can be "Green","Red","Red-Yellow" and "Yellow"

timeRed = 0.0
timeRedYellow = 0.0
timeGreen = 0.0
timeYellow = 0.0
m_start_signal = 1
workArray=[ 10.,1.,3.,10.,2.,"Green"]


current_milli_time = lambda: int(round(time.time() * 1000))		#these so-called lambda functions can be used anywhere a function is required.
	
def on_connect(client, userdata, flags, rc):
		print("Connected with result code "+str(rc))
		#self.client.subscribe(timestamp)
		client.subscribe(iRed)
		client.subscribe(iRedYellow)
		client.subscribe(iGreen)
		client.subscribe(iYellow)
		client.subscribe(TTNS)
		client.subscribe(interupt)
		client.subscribe(CS)
		client.subscribe(startTopic)
		
def on_message(client, userdata, msg):
	'''
	if self.msg.topic == timestamp:
			servertime = str(msg.payload)
			print("UTC Servertime:" +servertime)
	'''

	if msg.topic == iRed: 
		timeRed = msg.payload
		#print("Red: " + timeRed)
		workArray[0] = timeRed
	
	if msg.topic == iRedYellow:
		timeRedYellow = msg.payload
		#print("RedYellow: " + timeRedYellow)
		workArray[1] = timeRedYellow

	if msg.topic == iYellow:
		timeYellow = msg.payload
		#print("Yellow: " + timeYellow)
		workArray[2] = timeYellow

	if msg.topic == iGreen:
		timeGreen = msg.payload
		#print("Green: " + timeGreen)
		workArray[3] = timeGreen

	if msg.topic == interupt:
		serverInterupt = msg.payload
		#print("Serverinterupt " + serverInterupt)

	if msg.topic == TTNS:
		ttns = msg.payload
		#print("timeTillNextState " + ttns +"[seconds]")
		workArray[4] = ttns

	if msg.topic == CS:
		currentState = msg.payload
		#print("currentState " + currentState)
		workArray[5] = currentState
	
	if msg.topic == startTopic:
		m_start_signal = msg.payload
		
		
'''
class driver(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		print("I was created")
		self.drive()
		
	def drive(self):
		while True:
			driveAlgorithm()
			
class testThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		print("Ahoi")
'''			
class connectMQTT(threading.Thread,):
	def __init__(self,Broker):
		threading.Thread.__init__(self)
		
		if Broker == 0:
			self.Broker="172.31.12.122"
		
		self.client = mqtt.Client()
		self.client.on_connect = on_connect
		self.client.on_message = on_message
		self.client.connect(Broker, 1883, 60)
		self.run()
		
	def run(self):
		while noInterupt == True:
		#print(timeNextGreenDeadline())
			self.client.loop_start()
			#time.sleep(0.1)
			print str(workArray)
			q.put(workArray[4])
			q.task_done
			self.client.loop_stop()

def driveAlgorithm(q):
	t0 = current_milli_time()
	print "I jumped into driveAlgorith()"
	#while Mbot_start() == 1:
	workArray [4] = q.get()
	q.task_done
	try:
		print "Mbot started!"
		if timeNextGreenStart() == "error":
			print "Error"
			#break
		#elif m_start_signal == 0:
			#break
		else:
			mbot_drive_straight(serial,start_speed,"forward")		    
			tta = start_distance/start_speedsi
			print("Startsignal is: ",str(m_start_signal))
			# wenn die Gruenphase erreicht werden kann, dann behalte Geschwindigkeit
			if timeNextGreenStart()< tta and workArray[4] > tta:
				mbot_drive_straight(serial,start_speed,"forward")
				#Mbot wuerde vor oder nach der Gruenphase ankommen
			elif timeNextGreenStart() > tta or workArray[4] < tta:
			
			#Mbot muss an der Ampel stoppen
				if timeNextGreenStart() > start_distance/min_speed:
					print "slowdown buddy!"
					slowdown()
					tnow = current_milli_time()
					distance = ((start_speedsi+min_speedsi)/2)*(tnow-t0)
					if distance >= start_distance:
						print "Halt stop, jetzt bremst der mBot"
						mbot_motor_stop()
						print "Funktioniert das hier?"
					
			#Geschwindigkeit wird angepasst, sodass Mbot bei gruen ankommt		
			else:
				new_speed = distance/timeNextGreenStart()
				mbot_drive_straight(serial,new_speed,"forward")
				print "Geschwindigkeit wird gedrosselt für Grüne Welle :)"
	except Exception:
		print Exception.message
		

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
		return "error"
		print "Time till next Green Deadline can not be calculated"
		
def slowdown():
	for new_speed in range(start_speed,min_speed):
		mbot_drive_straight(serial,new_speed,"foreward")
		new_speed= new_speed-1
		sleep(0.2)

def main():
	print "Main Started here"
	q = Queue.LifoQueue()
	print "*** LIFO Queue created"
	
	try:
		print "MQTT should start here"
		mqttConnection = connectMQTT(Broker,q)
		mqttConnection.start()
		
		q.join()  
		
		print "Driver should start here"
		driveThread = Thread(target = driveAlgorithm, args=(q,))
		driveThread.setDaemon(True)
		driveThread.start()
		
	except Exception:
		Exception.message
	
	while True:
		pass
	
	#tTest = testThread()
	#tTest.start
	#tTest.setDaemon(True)
	
	#testDriver = driver()
	#testDriver.start()
	#testDriver.setDaemon(True)
	


	
	#driveAlgorithm()
	#threading.Thread(target=driveAlgorithm, args=())
	#alternative Thread start
	#start_new_thread(driveAlgorithm,())
	
if __name__ == '__main__':
	main()


