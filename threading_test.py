
#Import our reqired Librarys
from threading import Thread
import paho.mqtt.client as mqtt
import serial
import time
from mbot import mbot_drive_straight
from mbot import mbot_motor_stop

# Global variables for MQTT Transfer
global timeRed 
global timeRedYellow 
global timeGreen
global timeYellow 
global m_start_signal
global workArray
global state
global TTNS
global timestamp 
global iRed 
global iRedYellow 
global iGreen 
global iYellow       
global interupt 
global CS 
global startTopic 
global currentState

# Subscribe Topics all starting with traffiLight/ for
state = "traffiLight/state"             # dummy topic
TTNS = "traffiLight/timeTillNextState"  # refreshed subtopic showing time till change in seconds
timestamp = "traffiLight/timestamp"     # UTC Servertime from Trafficlight !!!Not needed yet"
iRed = "traffiLight/iRed"               # interval for Red in Seconds
iRedYellow = "traffiLight/iRedYellow"   # interval for Red-Yellow in Seconds
iGreen = "traffiLight/iGreen"           # interval for Green in Seconds
iYellow = "traffiLight/iYellow"         # interval for Yellow in Seconds
interupt = "traffiLight/interupt"       # interupt if Bus/RTW comes and other
CS = "traffiLight/currentState"         # current state as string, can be "Green","Red","Red-Yellow" and "Yellow"
startTopic = "traffiLight/start"        # topic to read start signal from for starting mBot from distance
currentState = ""                       # can be "Green","Red","Red-Yellow" and "Yellow"

timeRed = 0.0                           # inital time before MQTT received a value
timeRedYellow = 0.0                     # inital time before MQTT received a value
timeGreen = 0.0                         # inital time before MQTT received a value
timeYellow = 0.0                        # inital time before MQTT received a value
m_start_signal = 1                      # inital time before MQTT received a value
workArray=[ 10.,1.,3.,10.,2.,"Green"]   # inital time before MQTT received a value

# create some global variables to transfer Data from one thread into an other
global cycle                            # global is needed to break up with the Main Loop
cycle = 0.0

global mqtt_return_value                # This is a variable to return the mqtt values
mqtt_return_value = 0                   # for testing reasons the default is 0

global mqtt_return_start                # This is a variable to start the Drive Algorithm
mqtt_return_start = 0                   # Default of these var is 0 for Not Starting; 1 = Start Drive Algorithm

global Broker                           # Broker is running via a dedicated windows pc... The MQTT.fx ,Broker is used on Windows(@Johannes?)
Broker = "172.31.12.122"                # Broker IP Adress

global topic_pub                        # Mqtt Topic to subscribe
topic_pub="traffiLight/carMessage"




class Get_MQTT:                         # Begining of the Get_MQTT Class
    def __init__(self):                 
        self._running = True

        if Broker == 0:
            self.Broker="172.31.12.122"
        
        self.client = mqtt.Client()
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.connect(Broker, 1883, 60)

    def terminate(self):                # Terminator of the Get_MQTT Class
        self._running = False 

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        #self.client.subscribe(timestamp)
        client.subscribe(iRed)
        client.subscribe(iRedYellow)
        client.subscribe(iGreen)
        client.subscribe(iYellow)
        client.subscribe(TTNS)
        client.subscribe(interupt)
        client.subscribe(CS)
        client.subscribe(startTopic)
        
    def on_message(client, userdata, msg):
        '''
        if self.msg.topic == timestamp:
                servertime = str(msg.payload)
                print("UTC Servertime:" +servertime)
        '''

        if msg.topic == iRed: 
            timeRed = msg.payload
            #print("Red: " + timeRed)
            workArray[0] = timeRed
        
        if msg.topic == iRedYellow:
            timeRedYellow = msg.payload
            #print("RedYellow: " + timeRedYellow)
            workArray[1] = timeRedYellow

        if msg.topic == iYellow:
            timeYellow = msg.payload
            #print("Yellow: " + timeYellow)
            workArray[2] = timeYellow

        if msg.topic == iGreen:
            timeGreen = msg.payload
            #print("Green: " + timeGreen)
            workArray[3] = timeGreen

        if msg.topic == TTNS:
            ttns = msg.payload
            #print("timeTillNextState " + ttns +"[seconds]")
            workArray[4] = ttns

        if msg.topic == CS:
            currentState = msg.payload
            #print("currentState " + currentState)
            workArray[5] = currentState
        
        if msg.topic == startTopic:
            m_start_signal = msg.payload







    def run(self):                      # beginning of the "MAIN LOOP" from these Thread 
        global mqtt_return_value        # declare the global var for the Class
        global mqtt_return_start        # declare the global Start Var for the Class

        while self._running:            # Start While Loop

            self.client.loop_start()    
            

            print str(workArray)        # Prints out the recived Messages
                        
            


            self.client.loop_stop()
            """
                In the following we have to implement our MQTT SUPscriber BLA BLA 
                Our return value is a global var called "mqtt_return_value"
                The Value of this Var is available in our main and also in other threds if the global var is declared in the class 
            """

            

            #If the Start topic is subscribed with 1 
            """
            if Mqtt.start == 1 
                mqtt_return_start = 1
            """



            ##########     TEST
            time.sleep(0.1) #One second delay
            mqtt_return_value = mqtt_return_value+1
            print "MQTT Thread"
            ##########     END TEST





class Drive_Algorithm:                  # Beginning of the Drive_Algorithm
    def __init__(self):
        self._running = True

    def terminate(self):                # Terminator for the Drive_Algortihm_Thread
        self._running = False  

    def run(self):                      # beginning of the "Main Loop" From these Thread
        global mqtt_return_value        # declare the global var for the class
        while self._running:            # Start While Loop 

            """
                In the following while loop is some space for the drive algorithm

                Mbot befehle
            """
            
            ##############     TEST
            time.sleep(0.1)#One second delay
            print mqtt_return_value
            ##############     END TEST





#Create Class Get_MQTT
Get_MQTT = Get_MQTT()
#Create Thread Get_MQTT_Thread
Get_MQTT_Thread = Thread(target=Get_MQTT.run) 
#Start Thread Get_MQTT_Thread
Get_MQTT_Thread.start()

#Create Class Drive_Algortihm
Drive_Algorithm = Drive_Algorithm()
#Create Thread Drive_Algortihm_Thread
Drive_Algorithm_Thread = Thread(target=Drive_Algorithm.run) 
"""
#Start Thread Drive_Algortihm_Thread
Drive_Algorithm_Thread.start()          #The Drive Algorithm should be starded later in the Code, when the Main gets the Start Value
"""



Exit = False                            # Exit flag for Breaking up with the main Loop 
while Exit==False:                      # while Exit flag == False => Do the Loop... A Possible Exit Situation is when the Mbot reaches its goal
    #Starting the Main Loop of the whole Programm 

    """
        This is the Main Loop...
        This is where the magic happened
    """

    #The Get_MQTT Thread is already starded if there is there is the Start Topic, Start the Drive Algorithm
    if (mqtt_return_start == 1):
        """
            Now the Mbot starts
        """
        #Start Thread Drive_Algortihm_Thread
        Drive_Algorithm_Thread.start()          


    
    ############### Some Test Code 

    print "Hier meldet sich die Main zu wort"
    time.sleep(0.1) #One second delay

    #Test if the returnvalue of the mqtt thread is valid 
    #print mqtt_return_value

    cycle = cycle + 0.1 
    #print cycle
    if (cycle > 5): Exit = True #Exit Program

    ############### END of Test

Drive_Algorithm.terminate()
Get_MQTT.terminate()
print "Goodbye :)"
