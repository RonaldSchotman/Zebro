from bluetooth import *

target_name = "TUD254265"
                #"HTC Desire HD A9191 MATJE DONT CONNECT"
target_address = None
nearby_devices = discover_devices()


for address in nearby_devices:
    if target_name == lookup_name( address ):
        target_address = address
        break
if target_address is not None:
    print ("found target bluetooth device with address ", target_address)
else:
    print ("could not find target bluetooth device nearby")
