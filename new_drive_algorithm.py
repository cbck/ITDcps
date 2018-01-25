"""
	This Function should replace the "old" Drive algorithm



	Ich habe keine Ahnung ob dieser Code ohne weiters auf dem Mbot funktioniert, 
	alle einzelnen Funktionen scheinen aber genau ihren zweck zu erfuellen. 

	Wir sollten das ganze jetzt noch in eine Klasse packen und es ggf. direkt heute 
	Nachmittag nach Interaktive Gestaltung ausprobieren. 

	Gute Nacht... Es ist jetzt 4:16 Uhr ;)

"""

#for testing reasons import the time library
import time				

#This functions tooks an Integer Value between 0 and 255 and returns a Speed Value in M/S
def int2speed(int_speed, max_power_speed):
	#Calculate the M/S rate for each step between 0 and 255
	 units_per_val = max_power_speed/255
	 #Calculate the actual Speed 
	 speed =  units_per_val * int_speed
	 return speed

#This function tooks an Speed Value in M/s and generates a Integer Value between 0 and 255
def speed2int(speed, max_power_speed):
	#Calculate the M/S rate for each Step between 0 and 255 
	units_per_val = max_power_speed/255
	#calculate the Integer Value for the Mbot
	int_speed = speed / units_per_val
	return int(int_speed)

#This function checks if it is possible to reach the next Green light with max Speed and 
#gives back the earliest time the mbot could reach the trafficlight
def calc_reachable_green_phase(speed, distance, time_to_next_green_start, time_green_interval):
	#first of all calculate the time to reach with the setted Speed to arrive at the trafficlight

	#init a Var for saving our new time
	time_to_earliest_green_start = 0

	#while forever
	while (1):

		# Break Condition : If the time to reach the next green Phase < time to earliest green_start break the Loop		
		if (distance/speed <= time_to_earliest_green_start):
			break

		#otherwise add the intervaltime for the next greenphase to the Variable
		time_to_earliest_green_start = time_to_earliest_green_start + time_green_interval
		
	return time_to_earliest_green_start
	
#This Function tooks the initial start speed, the time to decide,  and the distance
def calc_rest_distance(start_speed, distance,t_decide):

	#at first calc the distance the Mbot has driven after he reaches t_decide 
	distance_before_decision = start_speed * t_decide

	#Than calculate the distance from t_decide to the trafficlight
	rest_distance = distance - distance_before_decision
	return rest_distance

#This Funktion is the real Drive Agorithm
def calc_new_speed(rest_distance, rest_time, time_offset):

	#add the offset to the rest time 
	rest_time = rest_time + time_offset

	#calc the new speed
	new_speed = rest_distance / rest_time
	return new_speed


"""
Here starts the Code 
"""

#there are a few given variables 

#time to next greed start give us the time till the next green phase beginns. 
#This Var is a Timer with an intervall of 10+1+3+10+2 = 26Sek.
time_to_next_green_start = 26.0 

#time intervall for the traffic light loop
time_green_interval = 26

#Max Power Speed is the Factor in M/s with MbotDrive(255 forward)
max_power_speed = 0.42

#seed is the setted maximum speed 
speed = 255

#time t is where the Mbot makes a Dessicion 
time_decide = 10

#distance from the Startingpoint to the Trafficlight
distance_start_trafficlight = 10

#time Offset to reach the trafficlight a little bit after switching
time_offset = 0

#Calc the first reachable green phase
earliest_green_phase = calc_reachable_green_phase(max_power_speed, distance_start_trafficlight, time_to_next_green_start, time_green_interval)#

#than calc the rest distance after time decision 
rest_distance = calc_rest_distance(max_power_speed, distance_start_trafficlight, time_decide)

#calc the time from t_desicion to time earliest green phase 
rest_time = earliest_green_phase - time_decide

#now calc the new Speed after time decision 
new_speed = calc_new_speed(rest_distance, rest_time, time_offset)

#now transfer the M/S value in an Mbot Vlaue
new_mbot_speed = speed2int(new_speed, max_power_speed)


#now we have all the paramters will need to controll the Mbot 

#Start the Mbot
mbot_drive_straight(serial,speed,"forward")

#now wait the time till t_decision
time.sleep(time_decide)

#now set the new Mobot Speed
mbot_drive_straight(serial,new_mbot_speed,"forward")

#now wait again till the mBot arrives the traffic light 
time.sleep(rest_time)

#After the Mbot should arrives its Goal 
mbot_motor_stop(serial)




"""

########## Sandbox ############

print int2speed(speed, max_power_speed)

print speed2int(int2speed(speed, max_power_speed), max_power_speed)

print calc_reachable_green_phase(max_power_speed, distance_start_trafficlight, time_to_next_green_start, time_green_interval)#

print calc_rest_distance(max_power_speed, distance_start_trafficlight, time_decide)

print new_speed

print new_mbot_speed

"""