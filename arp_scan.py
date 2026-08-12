from scapy.all import ARP,Ether,srp
"""
Burada Scapy'den üç şey alıyoruz:
Ether → Ethernet frame oluşturmak için
ARP → ARP paketi oluşturmak için
srp → Layer 2 seviyesinde paketi gönderip cevapları almak için
"""

def arp_ping(ip_str,timeout=2):
    packet = Ether(dst = "ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_str) # "/" scapy katman birleştirme operatörü L2 ve L3
    try:
        answered, unanswered = srp(
            packet,
            timeout=timeout,
            verbose=False # Scapy'nin terminale gereksiz bilgiler basmasını engelliyoruz.
        )
    except PermissionError:
        raise PermissionError(
            "Root privileges are required for ARP scanning. "
            "Please run the program with 'sudo'."
        )
    if answered:
        return answered[0][1].hwsrc # "hwsrc" donanım kaynağı
    else:
        return None

def arp_scan(cidr_str,timeout=2):
    packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=cidr_str)

    try:
        answered, unanswered = srp(
            packet,
            timeout=timeout,
            verbose=False
        )
    except PermissionError:
        raise PermissionError(
            "Root privileges are required for ARP scanning. "
            "Please run the program with 'sudo'."
        )

    result = {}
    for sent,received in answered:
        result[received.psrc] = received.hwsrc
    return result