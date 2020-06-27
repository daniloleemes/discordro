#!/bin/python3

import socket
import ipaddress

sock = socket.socket()
sock.connect(('127.0.0.1', 5121))
sock.send(bytes(''.encode('ASCII')))
sock.send(bytes('89DEADBEAF'.encode('ASCII')))

sock.send(bytes('19DEADBEAF'.encode('ASCII')))
sock.send(bytes('32DEADBEAF'.encode('ASCII')))


sock.close()
