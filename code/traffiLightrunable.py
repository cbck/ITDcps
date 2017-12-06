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
#standardlatency 120...200ms for Online MQTT network

red_LED = LED(25)
yellow_LED = LED(24)
green_LED = LED(23)
noInterupt = True

timeRed = 10
timeGreen = 10
timeRedYellow = 1
timeYellow = 3
 
Broker = "172.31.12.122"
sub_msg = "car/message"
pub_msg = "traffiLight/state" #state is exchange point for all paramters []
TTNS = "traffiLight/timeTillNextState"
DONS = "traffiLight/durationOfNextState"
AS = "traffiLight/actualState"
NS = "traffiLight/nextState"

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
		
		# Red Stage
		ttns = timeRed
		for idx in range(0,timeRed):
			red_LED.on()
			ttns = ttns -1
			#part for testing under one topic
			#client.publish(pub_msg,"TraffiState: RED - Seconds till change:")
			#client.publish(pub_msg,idx)
			
			client.publish(AS, "Red")
			client.publish(NS, "Red-Yellow")
			client.publish(TTNS, ttns)
			client.publish(DONS, timeRedYellow)
			print("AS=Red")
			print("NS=Red-Yellow")
			print(ttns)
			print(timeRedYellow)


			sleep(1)				
			idx-1
		 
		 
		# Stage Red - Yellow
		ttns = timeRedYellow
		yellow_LED.on()
		#client.publish(pub_msg,"TraffiState: YELLOW - red for 1sec")
		print("AS=Red-Yellow")
		print("NS=Green")
		print(ttns)
		print(timeRedYellow)
		client.publish(AS, "Red-Yellow")
		client.publish(NS, "Green")
		client.publish(TTNS, ttns)

		client.publish(DONS, timeGreen)
		sleep(timeRedYellow)
				
		red_LED.off()
		yellow_LED.off()
		
		# Green Stage
		ttns = timeGreen
		for idx in range(0,timeGreen):
			ttns=ttns-1
			#for testing under one topic
			#client.publish(pub_msg,"TraffiState: GREEN - Seconds till change:")
			#client.publish(pub_msg,idx)		

			client.publish(AS,"Green")
			client.publish(NS,"Yellow")
			print("AS=Green")
			print("NS=Yellow")
			print(ttns)
			print(timeRedYellow)
			client.publish(TTNS,ttns)
			client.publish(DONS,timeYellow)		
			green_LED.on()
			sleep(1)
			idx-1
		green_LED.off()
		

		#Yellow Stage
		ttns = timeYellow
		for idx in range(0,timeYellow):
			ttns = ttns-1
			yellow_LED.on()
			#client.publish(pub_msg,"TraffiState: YELLOW - Seconds till change:")
			#client.publish(pub_msg,idx)	
			print("AS=Yellow")
			print("NS=Red")	
			print(ttns)
			print(timeRedYellow)
			
			client.publish(AS,"Yellow")
			client.publish(NS,"Red")
			client.publish(TTNS,ttns)
			client.publish(DONS,timeRed)	
			sleep(1)
			idx-1
		yellow_LED.off()
			
client.loop_forever()

