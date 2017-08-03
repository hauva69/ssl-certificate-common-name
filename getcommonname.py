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
    except socket.gaierror as ex:
        logging.error('IP not found for host {0}: {1}'.format(host, ex))
        return False
    except UnicodeError as ex:
        logging.error('Check the certificate manually for host {0}: {1}'.format(host, ex))
    except TypeError as ex:
        logging.error('Check the certificarte manully for host {0}: {1}'.format(host, ex))
    result = sock.connect_ex((ip, port))
    if result == 0:
        return True
    else:
        return False

def main():
    for line in sys.stdin:
        host = line.strip()
        logging.debug(host)
        if is_port_open(host, 443):
            print('host={0}'.format(host))
            cmd = "/bin/echo | /usr/bin/openssl s_client -showcerts -connect {0}:443 2>&1 | /usr/local/bin/awk '/^subject=.*CN=/'".format(host)
            logging.debug('host={0}'.format(host))
            logging.debug(cmd)
            rc = os.system(cmd)
            if rc != 0:
                logging.debug('openssl exited with value {0} for hostname {1}'.format(rc, host))
                sys.exit(rc)

if __name__ == '__main__':
    main()
