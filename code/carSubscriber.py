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

servertime = ''

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(time)
    client.subscribe(iRed)
    client.subscribe(iRedYellow)
    client.subscribe(iGreen)
    client.subscribe(iYellow)
    client.subscirbe(TTNS)
    client.subscribe(interupt)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(Broker, 1883, 60) 
#timeSync  
    ts = time.time(ts)
    localtime = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S:%f')
    if msg.topic == time
        servertime = msg.payload
        if servertime != localtime
        localtime = servertime

    if msg.topic == iRed
        timeRed = msg.payload
    if msg.topic == iRedYellow
        timeRedYellow = msg.payload
    if msg.topic == iYellow
        timeYellow = msg.payload
    if msg.topic == iGreen
        timeGreen = msg.payload
    if msg.topic == interupt
        serverInterupt = msg.payload
    
client.loop_forever()
