#!/usr/bin/env python3

import socket
import sys

socket.setdefaulttimeout(10)
TCP_PORT = 502
BUFFER_SIZE = 1024
MESSAGE = b'\x00\x00\x00\x00\x00\x05\x00\x2b\x0e\x02\x00'

def validate(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        try:
            s.connect((ip, TCP_PORT))
        except Exception as ex:
            # unable to connect
            return None, str(ex)

        try:
            s.send(MESSAGE)
            data = s.recv(BUFFER_SIZE)
            msg = f"> received data: {data}"
            if not data:
                # connection closed; matches signature
                return True, msg
            return False, msg

        except Exception as ex:
            return False, str(ex)
    finally:
        s.close()

if __name__ == '__main__':
    print(validate(sys.argv[1]))
