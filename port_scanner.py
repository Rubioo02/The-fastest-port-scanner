import socket
import argparse
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored


def get_ip():

    parser = argparse.ArgumentParser(description='TCP PORT SCANNER')
    parser.add_argument("-i", "--ip", dest="ip", required=True, help="The '-i' or '--ip' parameter is to indicate the ip to which we want to scan the ports. (Ex: -i 102.168.1.1)")
    parser.add_argument("-p", "--port", dest="port", required=True, help="The '-p' or '--port' parameter is to indicate the range of ports to scan. (Ex1: -p 1-8080) (Ex2: -p 22,80,443) (Ex3: -p 22)")
    options = parser.parse_args()

    return options.ip, options.port

def ssocket():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)

    return s

def port_scanner(port, ip):

    s = ssocket()
    try:
        s.connect((ip,port))
        print(colored(f"\n [+] The port {port} is open", 'green'))
        s.close()
    except (socket.timeout, ConnectionRefusedError):
        s.close()

def launcher(ports, ip):

    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(lambda port: port_scanner(port, ip), ports)

def port_filtering(ports):

    if '-' in ports:
        first, last = map(int, ports.split('-'))
        return range(first, last+1)
    elif ',' in ports:
        return map(int, ports.split(','))
    else:
        return (int(ports),)

def main():

    ip, ports = get_ip()
    port = port_filtering(ports)
    launcher(port, ip)

if __name__ == '__main__':
    main()
