#!/usr/bin/env python3

'''
Reads a list of hostnames to check from stdin and runs 

echo | openssl s_client -showcerts -connect www.example.com:443 2>/dev/null |egrep subject=/CN
subject=/CN=*.example.com

on every line.
'''

import logging
import os
import socket
import sys

logging.basicConfig(level=logging.DEBUG)

def is_port_open(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = None
    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        return False
    result = sock.connect_ex((ip, port))
    if result == 0:
        return True
    else:
        return False

def main():
    for line in sys.stdin:
        line = line.strip()
        logging.debug(line)
        if is_port_open(line, 443):
            cmd = "/bin/echo | /usr/bin/openssl s_client -showcerts -connect {0}:443 2>/dev/null | /usr/local/bin/awk '/kauppalehti\.fi/ && /CN=/'".format(line)
            logging.debug(cmd)
            print(line, ': ',)
            rc = os.system(cmd)
            if rc != 0:
                logging.debug('openssl exited with value {0} for hostname {1}'.format(rc, line))
                sys.exit(42)

if __name__ == '__main__':
    main()
