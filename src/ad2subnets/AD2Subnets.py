#!/usr/bin/env python3

import sys
from .call_other_script import call_other_script_programmatically, find_script
from . import parse_args, subnets_from_csv


def assemble_command(args):
    auth_string, target = args.target.rsplit("@", 1)
    auth_string, password = auth_string.rsplit(":", 1)
    domain, username = auth_string.rsplit("/", 1)

    command = [
        target,
        "-u",
        f"{domain}\\{username}",
        "-p",
        f"{password}",
        "-r"
    ]
    return command

def write_file(subnets, output_filename):
    if not output_filename:
        return

    with open(output_filename, "w") as output_file:
        for subnet in subnets:
            output_file.write(f"{subnet}\n")

    print(f"Wrote {len(subnets)} subnets to {output_filename}")


def main() -> None:
    args = parse_args.main()
    print(args.csv_path)
    call_other_script_programmatically(assemble_command(args), module_path=find_script("adidnsdump.py"))
    try:
        subnets = subnets_from_csv.main(args.csv_path, -1, ",")
    except FileNotFoundError:
        print(f"Error: file not found: {args.csv_path}", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: permission denied: {args.csv_path}", file=sys.stderr)
        sys.exit(1)

    subnets = sorted(subnets, key=lambda n: int(n.network_address))

    print(f"\nSubnets Found:")
    # Print one subnet per line, sorted by network address
    for net in subnets:
        print(str(net))

    write_file(subnets, args.output)

if __name__ == "__main__":
    main()