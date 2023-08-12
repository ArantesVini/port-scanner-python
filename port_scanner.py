#!/usr/bin/python3

import sys, socket, multiprocessing, argparse
from main_ports import MAIN_PORTS


def port_scan(host, port, protocol):
    s = socket.socket(socket.AF_INET, protocol)
    s.settimeout(10)
    if s.connect_ex((host,int(port))) == 0:
        print(f"Port {port}/{protocol} open")

def multi_process(host, port_scan, port, protocol):
    l = multiprocessing.Process(target=port_scan, args=(host,str(port),protocol))
    l.start()

def write_results_to_file(results, filename):
    with open(filename, 'w') as f:
        for result in results:
            f.write(result + '\n')

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-m","--mainports", help="Perform a Scan on the 1000 main TCP ports", action="store_true")
    group.add_argument("-p","--ports", help="Specify ports for scan (separated by comma or hyphen)")
    parser.add_argument("-r", "--range", help="Specify a range of ports to scan (e.g. 1-1024)")
    parser.add_argument("-o", "--output", help="Specify a file to output the results to")
    parser.add_argument("ip",help="IP or domain for scanning")
    args = parser.parse_args()

    try:
        host = socket.gethostbyname(args.ip)
    except socket.gaierror:
        print("Invalid host, try again")
        sys.exit(1)

    if args.mainports:
        ports = MAIN_PORTS
        protocols = [socket.SOCK_STREAM] * len(ports)
    elif args.ports:
        ports = args.ports
        protocols = [socket.SOCK_STREAM] * len(ports.split(","))
    elif args.range:
        start, end = args.range.split("-")
        ports = range(int(start), int(end) + 1)
        protocols = [socket.SOCK_STREAM] * len(ports)
    else:
        print("Args error")
        sys.exit(1)

    results = []
    for i, port in enumerate(ports):
        protocol = protocols[i]
        multi_process(host, port_scan, port, protocol)
        results.append(f"Port {port}/{protocol} closed")

    if args.output:
        write_results_to_file(results, args.output)

if __name__ == "__main__":
    main()
