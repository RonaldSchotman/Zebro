#!/usr/bin/env python
# TU Delft Pico Zebro Demo
# bluetooth.py is for connecting to multiple PicoZebro's through bluetooth
# Writer: Martijn de Rooij
# Version 0.01

#hci0:	Type: BR/EDR  Bus: UART
#	BD Address: B8:27:EB:D6:C3:E1  ACL MTU: 1021:8  SCO MTU: 64:1
#	UP RUNNING 
#	RX bytes:61441 acl:17 sco:0 events:619 errors:0
#	TX bytes:4940 acl:16 sco:0 commands:219 errors:0


# Python 3 compatability
from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass

#/usr/bin/env python

import time
import bluetooth
#from wakeonlan import *


#phone = "ff:ff:ff:ff:ff:ff"

#def search():         
#  devices = bluetooth.discover_devices(duration = 5, lookup_names = True)
#  return devices

#while True:
#    results = search()
#    print(results)

print("performing inquiry...")

nearby_devices = bluetooth.discover_devices(
        duration=8, lookup_names=True, flush_cache=True, lookup_class=False)

print("found %d devices" % len(nearby_devices))

for addr, name in nearby_devices:
    try:
        print("  %s - %s" % (addr, name))
    except UnicodeEncodeError:
        print("  %s - %s" % (addr, name.encode('utf-8', 'replace')))

