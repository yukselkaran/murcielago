import time

from ping_sweep import scan_subnet_subprocess


CIDR = "192.168.1.0/28"
TIMEOUT = 0.2

for workers in [1, 5, 10, 25, 50]:
    print(f"Testing {workers} workers...")

    start = time.perf_counter()

    alive = scan_subnet_subprocess(
        CIDR,
        max_workers=workers,
        timeout=TIMEOUT
    )

    elapsed = time.perf_counter() - start

    print(
        f"workers={workers:3} | "
        f"time={elapsed:.3f}s | "
        f"alive={len(alive)}"
    )