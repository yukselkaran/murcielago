from scapy.all import ARP,Ether,srp
from subnet_calc import analyze_cidr

def arp_ping(ip_str,timeout=2):
    packet = Ether(dst = "ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_str) # "/" scapy katman birleştirme operatörü L2 ve L3
    answered , unanswered = srp(packet,timeout=timeout,verbose=False)
    if answered:
        return answered[0][1].hwsrc # "hwsrc" donanım kaynağı
    else:
        return None

def arp_scan(cidr_str,timeout=2):
    packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=cidr_str)
    answered, unanswered = srp(packet, timeout=timeout, verbose=False)

    result = {}
    for sent,received in answered:
        result[received.psrc] = received.hwsrc
    return result


if __name__ == "__main__":
    print(arp_ping("192.168.1.1"))    # router MAC beklenir
    print(arp_ping("192.168.1.250"))  # None beklenir

    result = arp_scan("192.168.1.0/24")
    for ip, mac in result.items():
        print(ip, "->", mac)