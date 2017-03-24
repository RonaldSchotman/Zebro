import wiringpi
wiringpi.wiringPiSetup()
serial = wiringpi.serialOpen('/dev/ttyS0',9600)
wiringpi.serialPuts(serial,'hello world!')
