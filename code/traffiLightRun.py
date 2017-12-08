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
timeRed = 10
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

stateMessage = []
interuptvariable = 0
#start to fill with t0 and
stateMessage[1] = t0 #t0 soll timestamp werden
stateMessage[2] = (t0 + timeRed)
stateMessage[3] = (t0 + timeRed + timeRedYellow) 
staeMessage[4] = (t0 + timeRed + timeRedYellow + timeGreen)
stateMessage[5] = (t0 + timeRed + timeRedYellow + timeGreen + timeYellow)
stateMessage[6] = interuptvariable


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
    ts = time.time(ts)
	t0 = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S:%f')
	client.publish(timestamp, t0)
	client.publish(iRed, timeRed)
	client.publish(iRedYellow, timeRedYellow)
	client.publish(iGreen, timeGreen)
	client.publish(iYellow, timeYellow)

	for idx in range(timeRed,0)
		red_LED.on()
		print("Red for " + idx + "s")
		client.publish(TTNS,idx)
		sleep(1)
		idx = idx-1
	
	for idx in range(timeRedYellow,0)
		yellow_LED.on()
		print("Red-Yellow for " + idx + "s")
		client.publish(TTNS,idx)
		sleep(1)
		idx = idx-1
	
	red_LED.off()
	yellow_LED.off()
	
	for idx in range(timeGreen,0)
		green_LED.on()
		print("Green for " + idx + "s")
		client.publish(TTNS,idx)
		sleep(1)
		idx = idx-1

	green_LED.off()

	for idx in range(timeYellow,0)
		yellow_LED.on()
		print("Green for " + idx + "s")
		client.publish(TTNS,idx)
		sleep(1)
		idx = idx-1

	yellow_LED.off		
	
client.loop_forever()

