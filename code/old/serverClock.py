#serverClock.py
#author Christopher.Beck@stud.hshl.de

import time
import datetime

ts = time.time()
#gives back the time since epoch (eg. 1970. 1st January 0:00 on C Libs)

st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
#2012-12-15 01:21:05

#Feedback Henkler
#Nachricht mit Timestamp

#t0,
#RedInterval,
#RedYellowInterval
#GreenInterval
#YellowInterval
#[Interrupt (einmal aperiodisch für Bus/RTW kernsignal anpassen)]

#Rechner(Server) hat Referenzuhr.
#Server verschickt immer wieder aktuelle Zeit. (ungenau, aber ok) (linearer anstieg)

#Client Uhr -> Clock Drift

#Systemzeit verschicken…

#Offset 
#t0 ist +5ms (Latenz)