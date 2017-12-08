import threading
import paho.mqtt.client as mqtt
import datetime
import time

'''
def publish_1(client,topic):
message="on"
print("publish data")
client.publish(topic,message)
publish_1(client,topic)
'''

Broker="172.31.12.122"
topic_pub="traffiLight/carMessage"
#subscribe topics
state = "traffiLight/state"             #dummy topic
TTNS = "traffiLight/timeTillNextState"  #refreshed subtopic showing time till change in seconds
time = "traffiLight/time"               #UTC Servertime from Trafficlight
iRed = "traffiLight/iRed"               #interval for Red in Seconds
iRedYellow = "traffiLight/iRedYellow"   #interval for Red-Yellow in Seconds
iGreen = "traffiLight/iGreen"           #interval for Green in Seconds
iYellow = "traffiLight/iYellow"         #interval for Yellow in Seconds
interupt = "traffiLight/interupt"       #interupt if Bus/RTW comes and other
timeRed = 0.0
timeRedYellow = 0.0
timeGreen = 0.0
timeYellow = 0.0
t0 = 0.0

servertime = ''
ts = 0.0

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe(time)
	client.subscribe(iRed)
	client.subscribe(iRedYellow)
	client.subscribe(iGreen)
	client.subscribe(iYellow)
	client.subscribe(TTNS)
	client.subscribe(interupt)

def on_message(client, userdata, msg):
	t0 = time.time()
	if msg.topic == time:
		servertime = (msg.payload)
	if msg.topic == iRed:
		timeRed = msg.payload
	if msg.topic == iRedYellow:
		timeRedYellow = msg.payload
	if msg.topic == iYellow:
		timeYellow = msg.payload
	if msg.topic == iGreen:
		timeGreen = msg.payload
	if msg.topic == interupt:
		serverInterupt = msg.payload
	
#def timeNextGreenDeadline():
	

def getPeriodTime():
	periodtime = timeRed + timeRedYellow + timeGreen + timeYellow
	return periodtime




client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(Broker, 1883, 60) 
#timeSync  

client.loop_forever()
