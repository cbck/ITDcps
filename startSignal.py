#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  startSignal.py
#  
#  Copyright 2018  <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  



# Python 3.4.2 (default, Oct 19 2014, 13:31:11) 
# [GCC 4.9.1] on linux
# Type "copyright", "credits" or "license()" for more information.
# project fifth semester - cps 
# authors Christopher Beck(christopher.beck(at)stud.hshl.de), Johannes Schaefer(johannes.schaefer(at)stud.hshl.de
# https://stackoverflow.com/questions/37006863/python-mqtt-script-on-raspberry-pi-to-send-and-receive-messages#37008092
# Client based version
# New more detailed States in Version 4


from time import sleep
import paho.mqtt.client as mqtt
import datetime
import time
#standardlatency 120...200ms for Online MQTT network

noInterupt = True
Broker = "172.31.12.122"
startTopic = "traffiLight/start"
	
# when traffiLight recieves Client-message, print topic and payload
def on_message(mqttc, userdata, msg):
	message = str(msg.payload)
	print(msg.topic+" "+message)

# when publishing message print message id
def on_publish(client, obj, mid):
    print("mid: " + str(mid))
    
 #create Client and try to connect to broker	
client = mqtt.Client()

client.on_message = on_message
client.connect(Broker, 1883, 60)
'''
while noInterupt == True:
	client.publish(startTopic,1)
	sleep()
'''

while 1:

	client.publish(startTopic,1)
	sleep(5)
	client.publish(startTopic,0)



