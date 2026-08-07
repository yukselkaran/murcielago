import struct
import socket
import os
import time

def checksum(data):
    # DEĞİŞMEDİ
    summation = 0
    for i in range(0, len(data) - 1, 2):
        summation += (data[i] << 8) + data[i + 1]
    if len(data) % 2:
        summation += data[-1] << 8
    while summation > 0xFFFF:
        summation = (summation & 0xFFFF) + (summation >> 16)
    return ~summation & 0xFFFF

def create_packet(identifier, sequence):
    # DEĞİŞMEDİ
    header = struct.pack("!BBHHH", 8, 0, 0, identifier, sequence)
    chksum = checksum(header)
    return struct.pack("!BBHHH", 8, 0, chksum, identifier, sequence)

def send_ping(sock, ip_str, identifier, sequence):
    pkt = create_packet(identifier, sequence)
    sock.sendto(pkt, (ip_str, 0))

def receive_pings(sock, pending, duration=2):
    alive = []
    deadline = time.time() + duration
    sock.settimeout(0.1)  # kısa timeout — döngüye geri dönüp deadline'ı kontrol edebilelim

    while time.time() < deadline and pending:
        try:
            data, addr = sock.recvfrom(1024)
        except socket.timeout:
            continue

        icmp_header = data[20:28]
        r_type, r_code, r_checksum, r_id, r_seq = struct.unpack("!BBHHH", icmp_header)

        if r_id == identifier and r_seq in pending:
            alive.append(pending[r_seq])
            del pending[r_seq]

    return alive