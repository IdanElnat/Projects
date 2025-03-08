import sys
import keyboard
from threading import Thread
import socket
import win32api
import time
from PIL import Image , ImageTk , ImageFile
import io
import tkinter as tk

ImageFile.LOAD_TRUNCATED_IMAGES = True


client_ip = "0.0.0.0"
KEY_PORT = 8182
MOUSE_PORT = 8183
SCREEN_PORT = 8184
def keyboard_listen():
    time.sleep(1)
    global stop_event
    key_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    key_server_socket.bind((client_ip, KEY_PORT))
    key_server_socket.listen()
    print("Keyboard Server is up and running")
    (key_socket, client_address) = key_server_socket.accept()
    print("Keyboard  Client connected")
    while not stop_event:
        event = keyboard.read_event()
        if(event.event_type == keyboard.KEY_DOWN):
            key_socket.send(event.name.encode())
        time.sleep(0.01)
def mouse_click_listen():
    time.sleep(1)
    mouse_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mouse_server_socket.bind((client_ip, MOUSE_PORT ))
    mouse_server_socket.listen()
    print("Mouse Server is up and running")
    (mouse_socket, client_address) = mouse_server_socket.accept()
    print("Mouse Client connected")
    global timer
    global stop_event
    timer = 0
    while not stop_event:
        time_since_updated_pos = time.time()
        if(win32api.GetKeyState(0x01) < 0):#left click
            mouse_socket.send("left_click".encode())
            print("clicked")
            time.sleep(0.01)
            while(win32api.GetKeyState(0x01) < 0):#left click hold
                if (timer >= time_to_update_pos_hold):
                    x_pos, y_pos = win32api.GetCursorPos()
                    pos = str(x_pos) + "," + str(y_pos)
                    mouse_socket.send(pos.encode())
                    timer = 0
                    time.sleep(0.01)
            mouse_socket.send("end_left_click".encode())


        if(win32api.GetKeyState(0x02) < 0):
            mouse_socket.send("right_click".encode())
            print("clicked")
            time.sleep(0.01)
            while (win32api.GetKeyState(0x02) < 0):  # left click hold
                if (timer >= time_to_update_pos_hold):
                    x_pos, y_pos = win32api.GetCursorPos()
                    pos = str(x_pos) + "," + str(y_pos)
                    mouse_socket.send(pos.encode())
                    timer = 0
                    time.sleep(0.01)
            mouse_socket.send("end_right_click".encode())
        elif (win32api.GetKeyState(0x03) < 0):
            mouse_socket.send("middle_click".encode())
            print("clicked")
        elif(timer >= time_to_update_pos):#checks if cooldown passed
            x_pos, y_pos = win32api.GetCursorPos()
            pos = str(x_pos) + "," + str(y_pos)
            mouse_socket.send(pos.encode())
            timer = 0
            time.sleep(0.01)
        time.sleep(0.1)

def screen_sharer():
    time.sleep(1)#gives time for "screen" to be set up
    global screen
    global stop_event
    image_label = tk.Label(screen,text="Waiting For User Connection...")
    image_label.pack() #creating the image displayer
    screen_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    screen_server_socket.bind((client_ip, SCREEN_PORT))
    screen_server_socket.listen()
    print("Screen sharer server started, waiting for connections...")
    (screen_socket, client_address) = screen_server_socket.accept()
    print("screen share started")

    while not stop_event:
        try:
            size_header = screen_socket.recv(4)
            while not size_header:
                size_header = screen_socket.recv(4)
            size_header = int.from_bytes(size_header , byteorder='big')
            img_data = b""

            while size_header > len(img_data):#recieves the image
                packet = screen_socket.recv(4096)
                print("reached")
                if not packet:
                    break
                img_data +=packet
            if(len(img_data) !=size_header):
                print("incorrect image data")
                continue#skip frame
            print("generating image")
            image = Image.open(io.BytesIO(img_data))
            tk_image = ImageTk.PhotoImage(image)

            image_label.config(image=tk_image)
            image_label.image = tk_image

            screen.update()#refresh UI
            time.sleep(1/120)
        except Exception as e:
            print(str(e))
            screen_socket.recv(1024)#clear garbage


def timer_seconds():
    global timer
    while True:
        timer +=0.01
        time.sleep(0.01)
def canvas():

    global screen
    screen = tk.Tk()
    screen.title("remoted PC screen , press ESC to close")
    screen.attributes('-fullscreen', True)
    tk.mainloop()
global screen

stop_event = False
timer = 0
time_to_update_pos = 0.05
time_to_update_pos_hold = 0.05

def main():
    global stop_event

    key_thread= Thread(target=keyboard_listen)
    mouse_thread = Thread(target=mouse_click_listen)
    time_thread =Thread(target=timer_seconds)
    canvas_thread = Thread(target=canvas)
    screen_thread = Thread(target=screen_sharer )


    key_thread.start()
    mouse_thread.start()
    screen_thread.start()
    time_thread.start()
    canvas_thread.start()

    print("waiting")
    keyboard.wait('esc')
    print("exit")
    stop_event = True #stops all threads
    sys.exit(0)




if __name__ == "__main__":
    main()