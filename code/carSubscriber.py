
import threading
import paho.mqtt.client as mqtt
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
state = "traffiLight/state"
TTNS = "traffiLight/timeTillNextState"
DONS = "traffiLight/durationOfNextState"
AS = "traffiLight/actualState"
NS = "traffiLight/nextState"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(AS)
    client.subscribe(NS)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(Broker, 1883, 60)
#thread1=threading.Thread(target=publish_1,args=(client,topic_pub))
#thread1.start()

client.loop_forever()
