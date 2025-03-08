import os


def check_ping(ip):
    response = os.system("ping -n 1 " + ip)
    if response == 0 :
        return True
    return False

def scan_network(network_prefix):
    active_ips = []
    for num in range (1,255):
        ip = "{}.{}".format(network_prefix,num)
        if check_ping(ip)== True:
            active_ips.append(ip)

    return active_ips

network_prefix = "192.168.68"
active_hosts = scan_network(network_prefix)
print(active_hosts)