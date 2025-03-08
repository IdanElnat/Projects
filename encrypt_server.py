import socket
import ssl


certfile = ''
keyfile = ''
socket = socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
socket.bind(("0.0.0.0" , 8889))
socket.listen()
socket = ssl.wrap_socket(socket, server_side= True , certfile = certfile,keyfile=keyfile)
client_socket ,addr = socket.accept()

message = client_socket.recv(1024).decode()
print(message)
client_socket.send("connected in encryption!".encode())
socket.close()
client_socket.close()

