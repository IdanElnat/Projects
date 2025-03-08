import itertools
import hashlib
import threading


import threads
def generate_passwords():
    words = "0123456789abcdefghijklmnopqrstuvwxyz"#set of password characters
    passwords = itertools.product(words , repeat = 8) #creates a 8 character combination
    return passwords

def copy_to_list(itertools_list):
    new_list = []
    for item in itertools_list:
        new_list.append("".join(item))

def calculate_md5(text):
    return hashlib.md5(text.encode()).hexdigest()
def decode_md5(hashed_password , possible_passwords):


    for password in possible_passwords:
        password = "".join(password)
        print("trying: {}".format(password))
        if(calculate_md5(password) == hashed_password):
            print("the password is : {}".format(password))
            return password
    print("password not found")
    return None
def main():
    possible_passwords = generate_passwords()
    possible_passwords = copy_to_list(possible_passwords)
    middle_index =  int(len(possible_passwords) / 2)
    start_to_middle = possible_passwords[:middle_index]
    middle_to_end = possible_passwords[middle_index+1::]
    start_to_middle_thread = threading.Thread(target = decode_md5() , args=(start_to_middle ,))
    middle_to_end_thread =  threading.Thread(target = decode_md5() , args=(middle_to_end ,))
    start_to_middle_thread.start()
    middle_to_end_thread.start()

    start_to_middle_thread.join()
    middle_to_end_thread.join()

if __name__ == "__main__":
    main()