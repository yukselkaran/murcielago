import struct
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