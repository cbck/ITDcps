# Python 3.4.2 (default, Oct 19 2014, 13:31:11) 
# [GCC 4.9.1] on linux
# Type "copyright", "credits" or "license()" for more information.
# project fifth semester - cps 
# authors Christopher Beck(christopher.beck(at)stud.hshl.de), Johannes Schaefer(johannes.schaefer(at)stud.hshl.de
# https://stackoverflow.com/questions/37006863/python-mqtt-script-on-raspberry-pi-to-send-and-receive-messages#37008092
# Client based version
# New more detailed States in Version 4

from gpiozero import LED
from time import sleep
import paho.mqtt.client as mqtt
import datetime
import time
#standardlatency 120...200ms for Online MQTT network

red_LED = LED(25)
yellow_LED = LED(24)
green_LED = LED(23)
noInterupt = True

#time in Seconds for different States
timeRed = 10 #s
timeGreen = 10
timeRedYellow = 1
timeYellow = 3
 
Broker = "172.31.12.122"
sub_msg = "car/message"
pub_msg = "traffiLight/state" #state is exchange point for all paramters []
#alternative
timestamp = "traffiLight/timestamp"
#intervals
iRed = "traffiLight/iRed"               #interval for Red in Seconds
iRedYellow = "traffiLight/iRedYellow"   #interval for Red-Yellow in Seconds
iGreen = "traffiLight/iGreen"           #interval for Green in Seconds
iYellow = "traffiLight/iYellow"         #interval for Yellow in Seconds
interupt = "traffiLight/interupt"       #interupt if Bus/RTW comes and other
TTNS = "traffiLight/timeTillNextState"
CS = "traffiLight/currentState"
t0 = ""




# when connecting to broker print result code
def on_connect(client, userdata, flags, rc):
	print("Connected:" +str(rc))
	client.subscribe(sub_msg, 0)
	
# when traffiLight recieves Client-message, print topic and payload
def on_message(mqttc, userdata, msg):
	message = str(msg.payload)
	print(msg.topic+" "+message)

# when publishing message print message id
def on_publish(client, obj, mid):
    print("mid: " + str(mid))
    
 #create Client and try to connect to broker	
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(Broker, 1883, 60)

while noInterupt == True:
	
	#Timestamp
	ts = time.time()
	t0 = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S:%f')
	print(ts)
	print(t0)
	client.publish(timestamp, t0)
	client.publish(iRed, timeRed)
	client.publish(iRedYellow, timeRedYellow)
	client.publish(iGreen, timeGreen)
	client.publish(iYellow, timeYellow)
	
	#First Stage: Red 
	yellow_LED.off()
	red_LED.off()
	green_LED.off()
	idx = (timeRed*10)
	n = (timeRed*10)
	ttns = float(timeRed)
	client.publish(CS,"Red")
	for idx in range(0,n):
		red_LED.on()
		sleep(0.1)
		ttns = ttns-0.1		
		idx = idx-1
		print("Red for %f")  % ttns
		client.publish(TTNS,ttns)
		
	#TimeStamp2
		
	ts = time.time()
	t0 = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S:%f')
	print(ts)
	print(t0)
	client.publish(timestamp, t0)
	
	#Second Stage: Red Yellow

	idx = (timeRedYellow*10)	
	n = timeRedYellow*10
	ttns = float(timeRedYellow)
	client.publish(CS,"Red-Yellow")
	for idx in range(0,n):
		ttns = ttns-0.1
		yellow_LED.on()
		print("Red-Yellow for %f") %ttns
		client.publish(TTNS,ttns)
		sleep(0.1)
		idx = idx-1
	
	red_LED.off()
	yellow_LED.off()
	
	#timeStamp3
	
	ts = time.time()
	t0 = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S:%f')
	print(ts)
	print(t0)
	client.publish(timestamp, t0)
	
	#Stage 3: Green
	
	idx =(timeGreen*10)
	n = timeGreen*10
	ttns = float(timeGreen)
	client.publish(CS,"Green")
	for idx in range(0,n):
		ttns = ttns-0.1
		green_LED.on()
		print("Green for %f") %ttns
		client.publish(TTNS,ttns)
		sleep(0.1)
		idx = idx-1

	green_LED.off()
	
	#Timestamp 4
	
	ts = time.time()
	t0 = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S:%f')
	print(ts)
	print(t0)
	client.publish(timestamp, t0)

	#Stage4 Yellow
	idx = (timeYellow*10)
	n = timeYellow*10
	ttns = float(timeYellow)
	client.publish(CS,"Yellow")
	for idx in range(0,n):
		ttns = ttns-0.1
		yellow_LED.on()
		print("Yellow for %f") %ttns
		client.publish(TTNS,ttns)
		sleep(0.1)
		idx = idx-1

	yellow_LED.off		
	
client.loop_forever()

