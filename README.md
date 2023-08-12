# Python Port Scanner

This is a simple, multi-process port scanner written in Python. It can scan a range of ports on a host and output the results to a file.

## Features

- Scans the 1000 main TCP ports
- Allows specifying a range of ports to scan
- Allows specifying individual ports to scan
- Outputs the results to a file

## Usage

`python portscanner.py [OPTIONS] IP`

### Options

- `-m, --mainports`: Perform a scan on the 1000 main TCP ports
- `-p, --ports`: Specify ports for scan (separated by comma or hyphen)
- `-r, --range`: Specify a range of ports to scan (e.g. 1-1024)
- `-o, --output`: Specify a file to output the results to

## Example

`python portscanner.py -m 192.168.1.1`

This will scan the 1000 main TCP ports on the host at 192.168.1.1.

## Dependencies

- Python 3
- argparse
- socket
- multiprocessing

## License

This project is licensed under the MIT License - see the [MIT LICENSE](LICENSE) file for details.
