import sys
import socket
import threading
import argparse

MAIN_PORTS = list(range(1, 1024))


def port_scan(host, port, protocol):
    s = socket.socket(socket.AF_INET, protocol)
    s.settimeout(10)
    if s.connect_ex((host, int(port))) == 0:
        print(f"Port {port}/{protocol} open")


def multi_process(host, port_scan, port, protocol):
    t = threading.Thread(target=port_scan, args=(host, str(port), protocol))
    t.start()


def write_results_to_file(results, filename):
    with open(filename, "w") as f:
        for result in results:
            f.write(result + "\n")


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-m",
        "--mainports",
        help="Perform a Scan on the 1000 main TCP ports",
        action="store_true",
    )
    group.add_argument(
        "-p", "--ports", help="Specify ports for scan (separated by comma or hyphen)"
    )
    parser.add_argument(
        "-r", "--range", help="Specify a range of ports to scan (e.g. 1-1024)"
    )
    parser.add_argument(
        "-o", "--output", help="Specify a file to output the results to"
    )
    parser.add_argument("ip", help="IP or domain for scanning")
    args = parser.parse_args()

    try:
        host = socket.gethostbyname(args.ip)
    except socket.gaierror:
        print("Invalid host, try again")
        sys.exit(1)

    def parse_ports(args):
        if "-" in args:
            start, end = [int(i) for i in args.split("-")]
            ports = list(range(start, min(end + 1, 65536)))
        else:
            ports = [int(p) for p in args.split(",")]
            ports = [p if p <= 65535 else 65535 for p in ports]
        protocols = [socket.SOCK_STREAM] * len(ports)
        return ports, protocols

    def parse_range(args):
        start, end = args.split("-")
        ports = range(int(start), min(int(end) + 1, 65536))
        protocols = [socket.SOCK_STREAM] * len(ports)
        return ports, protocols

    def parse_mainports(args):
        ports = MAIN_PORTS
        protocols = [socket.SOCK_STREAM] * len(ports)
        return ports, protocols

    def parse_args(args):
        parse_functions = {
            "ports": parse_ports,
            "mainports": parse_mainports,
            "range": parse_range,
        }

        for arg, func in parse_functions.items():
            if getattr(args, arg):
                return func(getattr(args, arg))

        print("Args error")
        sys.exit(1)

    ports, protocols = parse_args(args)

    results = []
    for i, port in enumerate(ports):
        protocol = protocols[i]
        multi_process(host, port_scan, port, protocol)
        results.append(f"Port {port}/{protocol} closed")

    if args.output:
        write_results_to_file(results, args.output)

    sys.exit(0)


if __name__ == "__main__":
    main()
