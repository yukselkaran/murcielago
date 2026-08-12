def ip_to_int(ip_str):
    ip_parts = ip_str.split(".") 
    #print(ip_parts)
    octets = [int(x) for x in ip_parts]
    result = 0
    for i in range(4):
        shift = 24 - (i * 8)
        result = result |  (octets[i] << shift)
    return result

def int_to_ip(ip_int):
    octet1 = (ip_int >> 24) & 0xFF
    octet2 = (ip_int >> 16) & 0xFF
    octet3 = (ip_int >> 8) & 0xFF
    octet4 = ip_int & 0xFF
    return f"{octet1}.{octet2}.{octet3}.{octet4}"

def cidr_to_mask_int(prefix_len):
    mask_int = (0xFFFFFFFF << (32 - prefix_len)) & 0xFFFFFFFF
    return mask_int

def get_network(ip_int,mask_int):
    network_int = ip_int & mask_int
    return network_int

def get_broadcast(network_int,mask_int):
    broadcast_int = network_int | (~mask_int & 0xFFFFFFFF)
    return broadcast_int

"""
 /31'de sadece 2 adres var (host biti = 1, yani 2^1 = 2 adres). 
 Bu 2 adresi "biri network biri broadcast" diye ayırırsan, geriye hiç host kalmaz — 
 bu da point-to-point bağlantılarda (iki router'ı birbirine bağlayan link gibi) israf olurdu. 
 Bu yüzden RFC 3021 standardı, /31 için network/broadcast ayrımını iptal etti — 
 her iki adres de host olarak kullanılabilir.

 /32'de ise sadece 1 adres var (host biti = 0). Burada network/broadcast kavramı bile anlamsız 
 — adres kendisiyle aynı. Genelde bu, "tek bir spesifik cihazı işaret et" için kullanılır 
 (örneğin router loopback interface'i, ya da bir cihazı static route ile tarif etmek).
 
 """

def get_host_count(prefix_len):
    if prefix_len == 32:
        return 1
    elif prefix_len == 31:
        return 2
    else:
        host_number = 2**(32-prefix_len) - 2
        return host_number
    
def get_host_range(network_int, broadcast_int, prefix_len):
    if prefix_len == 32:
        return network_int, network_int   # tek adres, hem ilk hem son kendisi
    elif prefix_len == 31:
        return network_int, broadcast_int   # ikisi de host
    else:
        first_host = network_int + 1
        last_host = broadcast_int - 1
        return first_host, last_host

def analyze_cidr(cidr_str):
    cidr_elements = cidr_str.split("/")

    prefix_len = int(cidr_elements[1])
    ip_int = ip_to_int(cidr_elements[0])

    mask_int = cidr_to_mask_int(prefix_len)
    network_int = get_network(ip_int,mask_int)
    broadcast_int = get_broadcast(network_int,mask_int)
    host_count = get_host_count(prefix_len)
    first_int,last_int = get_host_range(network_int,broadcast_int,prefix_len)

    ip_str = int_to_ip(ip_int)
    network_str = int_to_ip(network_int)
    broadcast_str = int_to_ip(broadcast_int)
    mask_str = int_to_ip(mask_int)
    first_str = int_to_ip(first_int)
    last_str = int_to_ip(last_int)

    result = {
        'cidr' : cidr_str,
        'ip' : ip_str,
        'prefix' : prefix_len,
        'mask' : mask_str,
        'network' : network_str,
        'broadcast' : broadcast_str,
        'first_host' : first_str,
        'last_host' : last_str,
        'host_count' : host_count
    }
    return result