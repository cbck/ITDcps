Python 3.4.2 (default, Oct 19 2014, 13:31:11)
[GCC 4.9.1] on linux
Type "copyright", "credits" or "license()" for more information.
# project fifth semester - cps 
# author christopher.beck(at)stud.hshl.de

from gpiozero import LED
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

red_LED = LED(25)
orange_LED = LED(24)
green_LED = LED(23)
noInterupt = True


#while init_count == 0:
        #init traffic lights, check for functionality
#       red_LED.on()
#       orange_LED.on()
#       green_LED.on()


#       time.sleep(3)
#       red_LED.off()
#       orange_LED.off()
#       green_LED.off()
#       print "Init succesfull"
#       init_count = 1


Broker = "192.168.0.112"
sub_msg = "car/message"
pub_msg = "traffiLight/state"


# when car connects to MQTT
def on_connect(client, userdata, flags, rc):
        print("Connected:" +str(rc))
        client.subscribe(sub_msg)


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
client.loop_start()


while noInetrupt == True:
                red_LED.on()
                sleep(10)
                client.publish("TraffiState: red for 10sec")

                orange_LED.on()
                client.publish("TraffiState: orange-red for 1sec")
                sleep(1)

                red_LED.off()
                orange_LED.off()
                client.publish("TraffiState: green for 10sec")
                green_LED.on()
                sleep(10)

                green_LED.off()
