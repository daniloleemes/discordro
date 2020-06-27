from dz_connect import dz_connect
from dz_msg_to_channel import dz_msg_to_channel
import binascii
import socket
import time
import select
from queue import Queue
from socket_data import socket_data

pkt = dz_connect()

print(pkt.get_header(as_string=True))

pkt.set_username('s1')
pkt.set_password('p1')
pkt.set_ip()
pkt.set_port(5131)
#pkt.pack()
data = pkt.get_data()


sd = socket_data()
sd.connect()
sd.send_packet(pkt)
sd.do_sockets()
time.sleep(3)
sd.do_sockets()
time.sleep(3)
pkt = dz_msg_to_channel()
pkt.set_username('discouser')
pkt.set_channel('#main')
pkt.set_message('It\'s from discord!')
sd.send_packet(pkt)
idx = 0
try:
    while 1:
        sd.do_sockets()
        pkt.set_message('Message #%d' % idx)
        sd.send_packet(pkt)
        idx += 1
        time.sleep(1)
except KeyboardInterrupt:
    pass
sd.close()