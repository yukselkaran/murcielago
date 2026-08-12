import os
import platform
import subprocess
import socket

from subnet_calc import analyze_cidr, ip_to_int, int_to_ip
from icmp_ping import send_ping, receive_pings
from concurrent.futures import ThreadPoolExecutor


def is_host_alive(ip_str, timeout=1):
    system = platform.system()

    if system == "Darwin":
        # macOS: -W milliseconds
        cmd = [
            "ping",
            "-c", "1",
            "-W", str(int(timeout * 1000)),
            ip_str
        ]

    elif system == "Linux":
        # Linux: -W seconds
        cmd = [
            "ping",
            "-c", "1",
            "-W", str(timeout),
            ip_str
        ]

    elif system == "Windows":
        # Windows: -w milliseconds
        cmd = [
            "ping",
            "-n", "1",
            "-w", str(int(timeout * 1000)),
            ip_str
        ]

    else:
        raise RuntimeError(
            f"Unsupported Operating System: {system}"
        )

    result = subprocess.run(
        cmd,
        stdout=subprocess.DEVNULL, # outputları terminal ekranına yazdırmamak için
        stderr=subprocess.DEVNULL # errorları terminal ekranına yazdırmamak için
    )

    return result.returncode == 0 # başarılı çalıştığında return 0 döndürür genel zaten c++ta da aynı 


def scan_subnet_icmp(cidr_str):
    result = analyze_cidr(cidr_str)
    first_int = ip_to_int(result["first_host"])
    last_int = ip_to_int(result["last_host"])

    try:
        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_RAW,
            socket.IPPROTO_ICMP
        )
    except PermissionError:
        raise PermissionError(
            "Root privileges are required. "
            "Please run the program with 'sudo'."
        )

    try:
        identifier = os.getpid() & 0xFFFF
        pending = {} # IP ler ile seq numaralarını eşleştiriyor.

        sequence = 0

        for ip_int in range(first_int, last_int + 1):
            ip_str = int_to_ip(ip_int)
            sequence += 1

            pending[sequence] = ip_str

            send_ping(
                sock,
                ip_str,
                identifier,
                sequence
            )

        alive = receive_pings(
            sock,
            pending,
            duration=2
        )

        return alive

    finally:
        sock.close()


def scan_subnet_subprocess(
    cidr_str,
    max_workers=50,
    timeout=1
):
    result = analyze_cidr(cidr_str)
    first_int = ip_to_int(result["first_host"])
    last_int = ip_to_int(result["last_host"])

    def worker(ip_str):
        return (
            ip_str
            if is_host_alive(ip_str, timeout)
            else None
        )

    ip_addresses = (
        int_to_ip(ip_int)
        for ip_int in range(first_int, last_int + 1)
    )

    with ThreadPoolExecutor(
        max_workers=max_workers
    ) as executor:

        results = executor.map(
            worker,
            ip_addresses
        )

    return [
        ip
        for ip in results
        if ip is not None
    ]


def scan_subnet(
    cidr_str,
    method="subprocess",
    max_workers=50,
    timeout=1
):
    if method == "icmp":
        return scan_subnet_icmp(cidr_str)

    return scan_subnet_subprocess(
        cidr_str,
        max_workers=max_workers,
        timeout=timeout
    )