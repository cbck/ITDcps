# Python 3.4.2 (default, Oct 19 2014, 13:31:11) 
# [GCC 4.9.1] on linux
# Type "copyright", "credits" or "license()" for more information.
# project fifth semester - cps 
# authors Christopher Beck(christopher.beck(at)stud.hshl.de), Johannes Schaefer(johannes.schaefer(at)stud.hshl.de
#https://stackoverflow.com/questions/37006863/python-mqtt-script-on-raspberry-pi-to-send-and-receive-messages#37008092
#Client based version

from gpiozero import LED
from time import sleep
import paho.mqtt.client as mqtt

red_LED = LED(25)
yellow_LED = LED(24)
green_LED = LED(23)
noInterupt = True
 
Broker = "172.31.12.122"
sub_msg = "car/message"
pub_msg = "traffiLight/state"


# when connecting to broker print result code
def on_connect(client, userdata, flags, rc):
	print("Connected:" +str(rc))
	client.subscribe(sub_msg, 0)
	
	
# when traffiLight recieves Client-message, print topic and payload

def on_message(client, userdata, msg):
	message = str(msg.payload)
	print(msg.topic+" "+message)

# when publishing message print message id
def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))
    
 #create Client and try to connect to broker	
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(Broker, 1883, 60)
		
while noInterupt == True:

		
		
		idx = 10
		
		for idx in range(0,10):
			red_LED.on()
			client.publish(pub_msg,"TraffiState: RED - Seconds till change:")
			client.publish(pub_msg,idx)
			sleep(1)				
			idx-1
		 
		yellow_LED.on()
		client.publish(pub_msg,"TraffiState: YELLOW - red for 1sec")
		sleep(1)
		
		red_LED.off()
		yellow_LED.off()
		
		idx = 10
		for idx in range(0,10):
			green_LED.on()
			client.publish(pub_msg,"TraffiState: GREEN - Seconds till change:")
			client.publish(pub_msg,idx)				
			sleep(1)
			idx-1
		
		green_LED.off()
		
		idx = 3
		for idx in range(0,3):
			yellow_LED.on()
			client.publish(pub_msg,"TraffiState: YELLOW - Seconds till change:")
			client.publish(pub_msg,idx)				
			sleep(1)
			idx-1
			
		yellow_LED.off()
client.loop_forever()
		
#while init_count == 0:
	#init traffic lights, check for functionality
#	red_LED.on()
#	orange_LED.on()
#	green_LED.on()


#	time.sleep(3)
#	red_LED.off()
#	orange_LED.off()
#	green_LED.off()
#	print "Init succesfull"
#	init_count = 1
