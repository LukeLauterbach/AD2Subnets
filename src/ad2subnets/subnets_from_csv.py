import csv
import ipaddress
from typing import Set

def main(path: str, col: int, delimiter: str) -> Set[ipaddress.IPv4Network]:
    subnets: Set[ipaddress.IPv4Network] = set()

    with open(path, newline="") as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row_num, row in enumerate(reader, start=1):
            if not row:
                continue
            # Normalize the column index against the row length
            idx = col if col >= 0 else len(row) + col
            if idx < 0 or idx >= len(row):
                # Column out of range for this row
                continue

            candidate = row[idx].strip()
            if not candidate:
                continue

            try:
                ip = ipaddress.ip_address(candidate)
            except ValueError:
                # Not an IP address
                continue

            # Only consider IPv4 for /24
            if isinstance(ip, ipaddress.IPv4Address):
                net = ipaddress.ip_network(f"{ip}/24", strict=False)
                subnets.add(net)

    return subnets