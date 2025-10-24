import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Get DNS records from AD and then parse them into subnets."
    )
    parser.add_argument(
        "target",
        help="[[domain/]username[:password]@]<targetName or address>"
    )

    parser.add_argument(
        '-o', '--output',
        help="(OPTIONAL) Filename to output subnets to"
    )

    args = parser.parse_args()
    args.csv_path = "records.csv"
    return args