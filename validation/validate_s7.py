#!/usr/bin/env python3

import socket
import sys

socket.setdefaulttimeout(10)
TCP_PORT = 102
BUFFER_SIZE = 1024
MESSAGE = b'\x03\x00\x00\x21\x02\xf0\x80\x32\x07\x00\x00\x00\x00\x00\x08\x00\x08\x00\x01\x12\x04\x11\x44\x01\x00\xff\x09\x00\x04\x00\x11\x00\x01'

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
            if len(data) >= 8 and data[7] == 0x32:
                # matches signature
                return True, msg
            return False, msg

        except Exception as ex:
            return False, str(ex)
    finally:
        s.close()

if __name__ == '__main__':
    print(validate(sys.argv[1]))
