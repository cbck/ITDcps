import threading
import paho.mqtt.client as mqtt
import datetime
import time
from time import sleep
from Queue import Queue
import pickle

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
startTopic = "traffiLight/start"
currentState = ""
timeRed = 0.0
timeRedYellow = 0.0
timeGreen = 0.0
timeYellow = 0.0
ttns = 0.0
t0 = 0.0
floats= 0.,0.,0.,0.,0.,str(currentState)
f = "io_file.txt"
servertime = ''
ts = 0.0
#qTTNS = Queue.LifoQueue(maxsize=0) #least in first out
q = Queue(maxsize =0)

def driveWithQueue(q):
	while True:
		print q.get()
		q.task_done()

def testQueue():
	worker = Thread(target=driveWithQueue, args=(q,))
	worker.setDaemon(True)
	worker.start()

class connectMQTT (threading.Thread):
	def __init__(self,Broker):
		threading.Thread.__init__(self)
		#if Broker == 0:
		#	self.Broker="172.31.12.122"
	
		self.client = mqtt.Client()
		self.client.on_connect = on_connect
		self.client.on_message = on_message
		self.client.connect(Broker, 1883, 60)

	def run(self):
		while True:
			#print(timeNextGreenDeadline())
			self.client.loop_forever()
	def getTTNS():
		return ttns
			

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe(timestamp)
	client.subscribe(iRed)
	client.subscribe(iRedYellow)
	client.subscribe(iGreen)
	client.subscribe(iYellow)
	client.subscribe(TTNS)
	client.subscribe(interupt)
	client.subscribe(CS)
	client.subscribe(startTopic)
	
def on_message(client, userdata, msg):
	t0 = time.time()
	
	if msg.topic == startTopic:
		startsignal = msg.payload
		if startsignal == 1:
			print("####################################### mBOT Start Signal ###################################")
		else:
			print("++++++++++++++++++++++++++++++++++++++++ STOP ++++++++++++++++++++++++++++++++++++++++++++++++")
			print(str(startsignal))

	if msg.topic == timestamp:
		servertime = str(msg.payload)
		print("UTC Servertime:" +servertime)
	
	if msg.topic == iRed:
		timeRed = msg.payload
		print("Red: " + timeRed)


	if msg.topic == iRedYellow:
		timeRedYellow = msg.payload
		print("RedYellow: " + timeRedYellow)

		
	if msg.topic == iYellow:
		timeYellow = msg.payload
		print("Yellow: " + timeYellow)


	if msg.topic == iGreen:
		timeGreen = msg.payload
		print("Green: " + timeGreen)

		
	if msg.topic == interupt:
		serverInterupt = msg.payload
		print("Serverinterupt " + serverInterupt)
		
	if msg.topic == TTNS:
		ttns = msg.payload
		print("timeTillNextState " + ttns +"[seconds]")
		#qTTNS.put(ttns)
		#qTTNS.task_done()
		q.put(ttns)
		q.task_done()

		
	if msg.topic == CS:
		currentState = msg.payload
		print("currentState " + currentState)


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
	#else return "file is opened by another process at the moment"
	
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
