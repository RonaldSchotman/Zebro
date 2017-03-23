import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5000

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)


sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

for i in range(100):
    sock.sendto(bytes([i, i, i, i]), (UDP_IP, UDP_PORT))
