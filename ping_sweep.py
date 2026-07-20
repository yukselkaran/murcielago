import subprocess
import threading
from subnet_calc import analyze_cidr, ip_to_int, int_to_ip

def is_host_alive(ip_str):
    result = subprocess.run(
        ['ping','-c','1','-W','1000',ip_str], # -c = packet count, -W = timeout süresi ::: ping -c 1 -W 1000 8.8.8.8 örnek yapı bu şekilde
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    if result.returncode == 0:
        return True
    else:
        return False
    
def scan_subnet(cidr_str):
    result = analyze_cidr(cidr_str)
    first_host = result["first_host"]
    last_host = result["last_host"]
    first_int = ip_to_int(first_host)
    last_int = ip_to_int(last_host)
    alive_hosts = []
    lock = threading.Lock()
    threads = []
    for ip_int in range(first_int,last_int + 1):
        ip_str = int_to_ip(ip_int)
        t = threading.Thread(target=worker,args=(ip_str,alive_hosts,lock))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return alive_hosts

def worker(ip_str, alive_list, lock):
    if is_host_alive(ip_str):
        with lock:
            alive_list.append(ip_str)

if __name__ == "__main__":
    print(is_host_alive("8.8.8.8"))          # True beklenir
    print(is_host_alive("192.168.1.250"))    # False beklenir (kendi ağına göre IP'yi değiştir)
    
    print("\nTarama başlıyor...")
    alive_hosts = scan_subnet("192.168.1.0/24")   # kendi ağına göre değiştir
    print("Canlı host'lar:", alive_hosts)