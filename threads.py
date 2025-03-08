from threading import Thread
from threading import Lock
def Thread1():
    global counter
    global lock
    for i in range(100000):
        with lock:
            counter +=1
        
def Thread2():
    global counter
    global lock
    for i in range(100000):
        with lock:
            counter -=1
       
        
        
if __name__ == "__main__":
    counter = 0
    lock = Lock()
    thread1 = Thread(target = Thread1)#creating two threads
    thread2 = Thread(target = Thread2)
    
    
    thread1.start()
    thread2.start()

    thread1.join()#waiting for the first to stop
    thread2.join()#waiting for the second to stop
    print(counter)