def checksum(data):
    summation = 0
    for i in range(0, len(data) - 1, 2):
        summation += (data[i] << 8) + data[i + 1]
    if len(data) % 2: 
        summation += data[-1] << 8
    while summation > 0xFFFF:
        summation = (summation & 0xFFFF) + (summation >> 16)
    return summation

if __name__ == "__main__":
    print(hex(checksum(b'\x08\x00\x00\x00\x30\x39\x00\x01')))
    # 0x383a beklenir
    
    print(hex(checksum(b'\xFF\xFF\xFF\xFF\xFF\xFF')))
    # 0xffff beklenir — taşma katlamayı test eder