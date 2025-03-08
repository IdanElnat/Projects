import keyboard
from threading import Thread
import socket
import time
import win32api, win32con , win32
from PIL import ImageGrab
import io

server_ip = "192.168.68.103"
KEY_PORT = 8182
MOUSE_PORT = 8183
SCREEN_PORT = 8184

def mouse_listen():
    mouse_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mouse_socket.connect((server_ip, MOUSE_PORT))
    print("Remotely connected")
    while True:
        try:
            input = mouse_socket.recv(1024).decode()
            if not input:
                continue
            if(input == "left_click"):
                print("left")
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, pos[0], pos[1])
                while ("end_left_click" not in input):
                    input = mouse_socket.recv(1024).decode()
                    if(len(input.split(",")) == 2 and "end_left_click" not in input):
                        pos = input.split(",")
                        pos = (int(pos[0]), int(pos[1]))
                        win32api.SetCursorPos(pos)
                        print("holding left")
                        input = mouse_socket.recv(1024).decode()
                print("finsihed hold")
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,pos[0],pos[1])
            elif (input == "right_click"):
                print("right")
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, pos[0], pos[1])
                while ("end_right_click" not in input):
                    input = mouse_socket.recv(1024).decode()
                    if(len(input.split(",")) == 2 and "end_right_click" not in input):
                        pos = input.split(",")
                        pos = (int(pos[0]), int(pos[1]))
                        win32api.SetCursorPos(pos)
                        print("holding right")
                        input = mouse_socket.recv(1024).decode()
                print("finsihed hold")
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, pos[0], pos[1])
            elif (input == "middle_click"):
                print("middle")
                win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, pos[0], pos[1])
                win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, pos[0], pos[1])
            elif (len(input.split(",")) == 2):
                pos = input.split(",")
                pos = (int(pos[0]), int(pos[1]))
                win32api.SetCursorPos(pos)
        except Exception as e:
            if "An existing connection was forcibly closed by the remote host" in str(e):
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,pos[0],pos[1])
                break
            print("messed input:" + str(e))
            mouse_socket.recv(1024)#throw garbage
            time.sleep(0.1)



def keyboard_listen():
    key_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    key_socket.connect((server_ip, KEY_PORT))
    print("Remotely connected")
    while True:
        try:
            input = key_socket.recv(1024).decode()
            print(input)
            if not input:
                continue
            keyboard.press_and_release(input)
        except Exception as e:
            if "An existing connection was forcibly closed by the remote host" in str(e):
                break
            print("messed input:" + str(e))
            key_socket.recv(1024)#throw garbage
            time.sleep(0.1)
def screen_sharer():
    screen_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    screen_client_socket.connect((server_ip, SCREEN_PORT))
    while True:
        try:
            screenshot = ImageGrab.grab()
            img_bytes = io.BytesIO()
            screenshot.save(img_bytes, format="PNG")# Save the screenshot to the bytes buffer in PNG format
            img_data=img_bytes.getvalue()
            screen_client_socket.send(len(img_data).to_bytes(4,byteorder='big'))
            screen_client_socket.sendall(img_data)
            time.sleep(1/30)
        except Exception as e:
            if "An existing connection was forcibly closed by the remote host" in str(e):
                break
            print("messed input:" + str(e))
            screen_client_socket.recv(1024)  # throw garbage
            time.sleep(0.1)

def main():
    while True:
        try:
            key_thread = Thread(target=keyboard_listen)
            mouse_thread = Thread(target=mouse_listen)
            screen_thread = Thread(target=screen_sharer)
            key_thread.start()
            mouse_thread.start()
            screen_thread.start()
        except:
            pass



if __name__ == "__main__":
    main()