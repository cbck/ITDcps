#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  timeTest.py
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

import time
from time import sleep
idx = True

# Paketempfangszeit herausfinden
# Zwischenspeichern und bei Anfrage mit einrechnen

def main():
	while idx == True:
		#print(time.time(),time.clock())
		#sleep(0.01)
		t0 = time.clock()
		sleep(2.5)
		print time.clock()
		
		t0 =time.time()
		sleep(2.5)
		print (time.time()-t0)
	
	return 0

if __name__ == '__main__':
	main()

