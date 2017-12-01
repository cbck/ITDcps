# Python 3.4.2 (default, Oct 19 2014, 13:31:11) 
# [GCC 4.9.1] on linux
# Type "copyright", "credits" or "license()" for more information.
# project fifth semester - cps 
# authors Christopher Beck(christopher.beck(at)stud.hshl.de), Johannes Schäfer(johannes.schaefer@stud.hshl.de
#https://stackoverflow.com/questions/37006863/python-mqtt-script-on-raspberry-pi-to-send-and-receive-messages#37008092
#procedural version

from gpiozero import LED
from time import sleep
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

red_LED = LED(25)
orange_LED = LED(24)
green_LED = LED(23)
noInterupt = True
 
Broker = "172.31.12.122"
sub_msg = "car/message"
pub_msg = "traffiLight/state"


# when car connects to MQTT
def on_connect(client, userdata, flags, rc):
	print("Connected:" +str(rc))
	client.subscribe(sub_msg, 0)
	
	
# when traffiLight recieves MQTT-message

def on_message(client, userdata, msg):
	message = str(msg.payload)
	print(msg.topic+" "+message)
	#display_traffistate
	#TODO
	
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(Broker, 1883, 60)

#def on_publish(client, userdata, mid):
		
while noInterupt == True:

		
		
		idx = 10
		
		for idx in range(0,10):
			red_LED.on()
			sleep(1)
			publish.single(pub_msg,"TraffiState: RED - Seconds till change",hostname= Broker)
			publish.single(pub_msg, idx,hostname= Broker)
			idx-1
		 
		orange_LED.on()
		publish.single(pub_msg,"TraffiState: orange-red for 1sec",hostname= Broker)
		sleep(1)
		
		red_LED.off()
		orange_LED.off()
		
		idx = 10
		for idx in range(0,10):
			publish.single(pub_msg,"TraffiState: GREEN - Seconds till change",hostname= Broker)
			publish.single(pub_msg,idx,hostname= Broker)			
			green_LED.on()
			sleep(1)
			idx-1
		
		green_LED.off()
		
		idx = 3
		for idx in range(0,3):
			orange_LED.on()
			publish.single(pub_msg,"TraffiState: Yellow - Seconds till change",hostname= Broker)
			publish.single(pub_msg,idx,hostname= Broker)
			sleep(1)
			idx-1
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
