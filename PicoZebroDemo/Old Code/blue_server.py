import bluetooth

bd_addr = "A4:17:31:F2:A7:88"#"F8:DB:7F:AC:70:D2" 
#bd_addr = "98:D3:31:50:0A:CE" //the address from the Arduino sensor
port = 1
sock = bluetooth.BluetoothSocket (bluetooth.RFCOMM)
sock.connect((bd_addr,port))
 
while True:
    tosend = raw_input()
    if tosend != 'q':
        sock.send(tosend)
    else:
        break
 
sock.close()
