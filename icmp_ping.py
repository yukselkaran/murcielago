import struct
import socket
import os 
import time
def checksum(data):
    summation = 0
    for i in range(0, len(data) - 1, 2):
        summation += (data[i] << 8) + data[i + 1]
    if len(data) % 2: 
        summation += data[-1] << 8
    while summation > 0xFFFF:
        summation = (summation & 0xFFFF) + (summation >> 16)
    return ~summation & 0xFFFF

def create_packet(identifier,sequence):
    header = struct.pack("!BBHHH",8,0,0,identifier,sequence)
    chksum = checksum(header)
    return struct.pack("!BBHHH",8,0,chksum,identifier,sequence)

def ping_host(ip_str,timeout=1):
    sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)
    sock.settimeout(timeout)
    identifier, sequence = (os.getpid() & 0xFFFF, 1)
    pkt = create_packet(identifier,sequence)
    sock.sendto(pkt, (ip_str,0))
    try:
        sock.recvfrom(1024)
        return True
    except socket.timeout:
        return False
    finally:
        sock.close()

if __name__ == "__main__":
    print(hex(checksum(b'\x08\x00\x00\x00\x30\x39\x00\x01')))
    # 0x383a beklenir
    
    print(hex(checksum(b'\xFF\xFF\xFF\xFF\xFF\xFF')))
    # 0xffff beklenir — taşma katlamayı test eder

    print(hex(checksum(b'\x08\x00\x00\x00\x30\x39\x00\x01')))
    # 0xc7c5 beklenir
    
    print(hex(checksum(b'\x08\x00\xc7\xc5\x30\x39\x00\x01')))
    # 0x0 beklenir

    paket = create_packet(12345, 1)
    print(paket)
    print(len(paket))            # 8
    print(hex(checksum(paket)))  # 0x0

    print(ping_host("8.8.8.8"))        # True beklenir
    print(ping_host("192.168.1.250"))  # False beklenir