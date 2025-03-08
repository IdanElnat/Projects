from tabnanny import check

import scapy.all as scapy
import subprocess


def get_ip(mac):#only of arp table isnt already poisoned so its called in the sniff only
    for pair in trusted_adresses:
        if pair['mac'] == mac:
            return pair['ip']

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
def get_all_macs():
    target_ip="192.168.68.1/24"
    # IP Address for the destination
    # create ARP packet
    arp = scapy.ARP(pdst=target_ip)
    # create the Ether broadcast packet
    # ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
    ether = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # stack them
    packet = ether / arp

    result = scapy.srp(packet, timeout=3, verbose=0)[0]

    # a list of clients, we will fill this in the upcoming loop

    try:
        devices = []
        for sent, received in result:
            # for each response, append ip and mac address to `devices` list
            devices.append({'ip': received.psrc, 'mac': received.hwsrc})
        for device in devices:
            print(f"MAC: {device['mac']}, IP: {device['ip']}")

        return devices
    except :
        return None


def sniff_arps(interface):
    print("sniffing")
    scapy.sniff(iface=interface, store=False, prn=process_packet)
def process_packet(packet):
    # checking if the packet is in the arp protocol
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        print("got an ARP pakacge(reply) ")
        print("checking for spoofing")
        sender_ip =packet[scapy.ARP].psrc
        response_mac = packet[scapy.ARP].hwsrc
        print(sender_ip, "sent an arp reply stating his mac is" , response_mac)
        while not new_arp_table:
            new_arp_table = get_all_macs()
        for pair in new_arp_table:
            if sender_ip in pair['ip'] and pair['mac'] != response_mac:#live spoof checking
                attacker_ip = get_ip(responsemac)
                victim_mac = pair['mac']
                print("<!> ARP table is being poisoned <!>")
                print("the attacker mac addres is {} and the ip adress is{}".format(responsemac, attacker_ip))
                print("the victims mac adress is {} nad the ip adress is {}".format(victim_mac, sender_ip))
                break
def is_attacker(mac , potential_attacker):
    is_matching_mac = mac == potential_attacker['mac']
    is_matching_ip - get_mac(potential_attacker['ip']) == potential_attacker['mac']
    return  is_matching_mac and  is_matching_ip
def spoof_detector(): # checking if already spoofed
    print("checking for spoofing")

    for pair1 in initial_arp_table:
        count_mac = 0 #how many times the same MAC adrress is in the table
        checked_mac = pair1['mac']
        for pair2 in initial_arp_table:
            if checked_mac == pair2['mac']:
                count_mac += 1
        if (count_mac > 1):
            print(checked_mac, " ", count_mac)
            for is_victim in initial_arp_table:
                if get_mac(is_victim['ip']) != is_victim['mac']:
                    victim_mac = get_mac(is_victim['ip'])
                    victim_ip = is_victim['ip']
                    for potential_attacker in trusted_adresses:#finding matching ip adrress to the attackers mac
                        if is_attacker(checked_mac , potential_attacker):
                            attacker_ip = potential_attacker['ip']
                            break
                    break
            print("<!> ARP table has been poisoned <!>")
            print("the attacker mac addres is {} and the ip adress is{}".format(checked_mac, attacker_ip))
            print("the victims mac adress is {} nad the ip adress is {}".format(victim_mac, victim_ip))




initial_arp_table = {}
while not initial_arp_table:
    initial_arp_table = get_all_macs()
def main():
    spoof_detector()  # checks if the table is already poisoned
    while True:
        sniff_arps("Ethernet")#checks sent ARP requests
if __name__ == "__main__":
    main()