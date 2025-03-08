import hashlib


def brute_force(hash):
    potential_pass= 0
    while(99999<potential_pass<1000000):
        new_hash = hashlib.md5(str(potential_pass).encode()).hexdigest()
        if(new_hash == hash):
            return potential_pass

        potential_pass+=1
    return None


def main():
    hash = input("enter the hash you want to decrypt")
    password = brute_force(hash)
    if password:
        print("hash decrypted , password is: " , password)
    else:
        print("couldnt crack hash")
if __name__ == "__main__":
    main()