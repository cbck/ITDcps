import threading
import paho.mqtt.client as mqtt
import datetime
import time
from time import sleep
import Queue
import pickle

'''
def publish_1(client,topic):
message="on"
print("publish data")
client.publish(topic,message)
publish_1(client,topic)
'''
noInterupt = True
Broker="172.31.12.122"
topic_pub="traffiLight/carMessage"
#subscribe topics
state = "traffiLight/state"             #dummy topic
TTNS = "traffiLight/timeTillNextState"  #refreshed subtopic showing time till change in seconds
timestamp = "traffiLight/timestamp"               #UTC Servertime from Trafficlight
iRed = "traffiLight/iRed"               #interval for Red in Seconds
iRedYellow = "traffiLight/iRedYellow"   #interval for Red-Yellow in Seconds
iGreen = "traffiLight/iGreen"           #interval for Green in Seconds
iYellow = "traffiLight/iYellow"         #interval for Yellow in Seconds
interupt = "traffiLight/interupt"       #interupt if Bus/RTW comes and other
CS = "traffiLight/currentState"
currentState = ""
timeRed = 0.0
timeRedYellow = 0.0
timeGreen = 0.0
timeYellow = 0.0
t0 = 0.0
floats= 0.,0.,0.,0.,0.,str(currentState)
f = "io_file.txt"

servertime = ''
ts = 0.0

class connectMQTT(threading.Thread):
	def __init__(self,Broker):
		threading.Thread.__init__(self)
		if Broker == 0:
			self.Broker="172.31.12.122"
	
		self.client = mqtt.Client()
		self.client.on_connect = on_connect
		self.client.on_message = on_message
		self.client.connect(Broker, 1883, 60) 	
		self.run()
		
	def on_connect(self,client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	self.client.subscribe(timestamp)
	self.client.subscribe(iRed)
	self.client.subscribe(iRedYellow)
	self.client.subscribe(iGreen)
	self.client.subscribe(iYellow)
	self.client.subscribe(TTNS)
	self.client.subscribe(interupt)
	self.client.subscribe(CS)
	
	def on_message(self,client, userdata, msg):
		t0 = time.time()

		if self.msg.topic == timestamp:
			servertime = str(msg.payload)
			print("UTC Servertime:" +servertime)
		
		if self.msg.topic == iRed:
			timeRed = msg.payload
			print("Red: " + timeRed)
			floats[0] = timeRed
			writeIO(floats,f)
	
		if self.msg.topic == iRedYellow:
			timeRedYellow = msg.payload
			print("RedYellow: " + timeRedYellow)
			floats[1] = timeRedYellow
			writeIO(floats,f)
		
		if self.msg.topic == iYellow:
			timeYellow = msg.payload
			print("Yellow: " + timeYellow)
			floats[2] = timeYellow
			writeIO(floats,f)

		if self.msg.topic == iGreen:
			timeGreen = msg.payload
			print("Green: " + timeGreen)
			floats[3] = timeGreen
			writeIO(floats,f)
		
		if self.msg.topic == interupt:
			serverInterupt = msg.payload
			print("Serverinterupt " + serverInterupt)
		
		if self.msg.topic == TTNS:
			ttns = msg.payload
			print("timeTillNextState " + ttns +"[seconds]")
			floats[4] = ttns
			writeIO(floats,f)
		
		if msg.topic == CS:
			currentState = msg.payload
			print("currentState " + currentState)
			floats[5] = currentState
			writeIO(floats,f)

	def run(self):
		while noInterupt == True:
			#print(timeNextGreenDeadline())
			self.client.loop_forever()


def getPeriodTime():
	periodtime = timeRed + timeRedYellow + timeGreen + timeYellow
	return periodtime

def writeIO(data, outfile):
	ifile = open(outfile, "wb")
	pickle.dump(data,ifile)
	ifile.close()
	
def readIO(filename):
	#@TODO if Abfrage falls file schon offen
	if closed(filename) == True:
		ifile = open(filename)
		data = pickle.load(ifile)
		ifile.close()
		return data
	else return "file is opened by another process at the moment"
	
def timeNextGreenDeadline():
	if 	currentState == "Green":
		return 0 

	elif currentState == "Red":
		return ((timeRed - ttns) + timeRedYellow)
		
	elif currentState == "Yellow":
		return ((timeYellow -ttns) + timeRed + timeRedYellow)
		
	elif currentState == "Red-Yellow":
		return ttns
	else:
		return "Time till next Green Deadline can not be calculated"
