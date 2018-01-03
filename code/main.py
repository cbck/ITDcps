#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#  
#  Copyright 2017  <pi@raspberrypi>
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

import MbotMQTT.py
import carSubscriber.py
import Queue	
from carSubscriber import 

#distance = 50.0

def main():
	if(timeNextGreenDeadline) == "error":
		break
			
    elif(timeNextGreenDeadline) == 0:
		mbot_drive_straight(my_mbot,serial,255,"forward")
	
	elif(timeNextGreenDeadline) < distance/mbot_speed:
		mbot_motor_stop
	
	elif(timeNextGreenDeadline) > distance/mbot_speed:
		mbot_speed = distance/timeNextGreenDeadline
		mbot_drive_straight(my_mbot,serial,mbot_speed,"forward")
	
	
	client.loop_forever()

if __name__ == '__main__':
	main()

