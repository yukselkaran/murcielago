import struct
import socket

"""
######################1############################
IPv4 header'ını ham byte'lardan alanlara ayırıyoruz.
"!" = Network byte order (big-endian)
B = 1 byte'lık alan
H = 2 byte'lık alan
4s = 4 byte'lık ham veri (IP adresleri)

######################2############################
socket.inet_ntoa() ham (raw) IPv4 adresini insanların okuyabileceği
standart noktalı IP adresine dönüştürür.
Örneğin:
4 byte'lık ham veri → b'\x08\x08\x08\x08'
inet_ntoa() → "8.8.8.8"
Yani struct.unpack() ile çıkardığımız src_raw ve dst_raw değerlerini
okunabilir IP adreslerine çevirmek için kullanacağız.
"""

def parse_ip_header(data): 
    version_ihl, tos, total_len, ident, flags_frag, ttl, proto, chksum, src_raw, dst_raw = struct.unpack("!BBHHHBBH4s4s", data[:20])

    version = version_ihl >> 4
    ihl = version_ihl & 0x0F
    header_length = ihl * 4

    src = socket.inet_ntoa(src_raw)
    dst = socket.inet_ntoa(dst_raw)
    return {
            "version": version,
            "ihl": ihl,
            "header_length": header_length,
            "ttl": ttl,
            "protocol": proto,
            "src": src,
            "dst": dst,
    }

if __name__ == "__main__":
    # test için ai ile örnek byte dizisi uydurdum
    ornek = bytes.fromhex("450000541c4600007501abcd08080808c0a80132")
    sonuc = parse_ip_header(ornek)
    print(sonuc)