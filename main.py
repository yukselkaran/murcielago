import argparse
from subnet_calc import analyze_cidr
from ping_sweep import scan_subnet
from arp_scan import arp_scan

def main():
    parser = argparse.ArgumentParser(description="Murciélago - subnet hesaplayıcı ve ağ tarayıcı")

    parser.add_argument("--cidr", required=True, help="CIDR notasyonu, örn 192.168.1.0/24")
    parser.add_argument("--scan", choices=["subprocess", "icmp", "arp"], help="Tarama yöntemi")

    args = parser.parse_args()
    info = analyze_cidr(args.cidr)
    print("=== Subnet Bilgisi ===")
    for key, value in info.items():
        print(f"{key}: {value}")

    if args.scan:
        print(f"\n=== Tarama ({args.scan}) ===")
        if args.scan == "arp":
            result = arp_scan(args.cidr)
            for ip, mac in result.items():
                print(f"{ip} -> {mac}")
        else:
            alive = scan_subnet(args.cidr, method=args.scan)
            for ip in alive:
                print(ip)


if __name__ == "__main__":
    main()