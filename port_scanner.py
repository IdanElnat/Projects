import socket

def main( dest_ip ):

    open_ports= []
    for port in range(1,65535):
        if(is_open(port , dest_ip)):
            open_ports.append(port)
    print("the open ports on {} are {}".format(dest_ip,open_ports))
def is_open(port , ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip, port))
    print("checking port {}".format(port))
    if result == 0:
        return True
    else:
        return False
    sock.close()
if __name__ == "__main__":
    main("142.250.75.110")