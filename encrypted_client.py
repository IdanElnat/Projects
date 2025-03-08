from cryptography.fernet import Fernet
path = r'C:\Users\User\OneDrive\Desktop\לימודים\מועדון המתכנתים\sandbox\image.jpg'
key = Fernet.generate_key()
fernet = Fernet(key)
print("encrypting...", path)
file = open(path, "rb")
data = file.read()
print(data)



encrypted_data = fernet.encrypt(data)
print(type(encrypted_data),"data:" , encrypted_data)
file = fernet.decrypt(encrypted_data)
print(type(file) ,"data:" , file)