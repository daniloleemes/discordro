import socket
import select
import struct
from packets import Packet, zd_packet_dict, dz_packet_dict


class socket_data:
    STATE_START = 0
    STATE_CONNECTING = 1
    STATE_CONNECTED = 2
    STATE_DISCONNECTED = 3

    def __init__(self, client, channels):
        self.server_username = 's1'
        self.server_password = 'p1'
        self.server_ip = '127.0.0.1'
        self.server_port = 5131
        self.sock = None
        self.rfifo = None
        self.wfifo = None
        self.eof = False
        self.state = self.STATE_START
        self.client = client
        self.channels = channels
        for ch in self.channels:
            ch['messages'] = []

    def connect(self):
        self.sock = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0)
        self.sock.connect((self.server_ip, self.server_port))
        self.sock.setblocking(False)
        self.rfifo = bytearray()
        self.wfifo = bytearray()
        self.state = self.STATE_CONNECTING
    
    def close(self):
        print('Closing connection to server')
        self.sock.close()
        self.sock = None
        self.rfifo = None
        self.wfifo = None

    def recv_to_fifo(self, length=1024):
        if not self.sock:
            return -1

        data = self.sock.recv(length, 0)
        
        if not data:
            print('recv_to_fifo: Server closed connection')
            self.eof = True
            return -1

        self.rfifo.extend(data)

        return 0

    def send_from_fifo(self):
        if not self.sock:
            return -1
        
        if len(self.wfifo) == 0:
            return 0
        print('Sent packet')
        length = self.sock.send(self.wfifo, 0)
        
        if length < 0:
            print('send_from_fifo: Server closed connection')
            self.eof = True
            return -1

        if length > 0:
            self.wfifo = self.wfifo[length:]
        
        return 0

    def parse_fifo(self):
        if not self.sock:
            return -1
            
        while len(self.rfifo) >= 2:
            cmd = Packet.parse_header(self.rfifo[:2])
            print(format(cmd, '#06x'))
            dlen = len(self.rfifo)
            print(dlen)
            cls = zd_packet_dict[cmd]
            print(cls)
            plen = cls.get_fmt_len()
            print(plen)

            if plen == -1:
                print('variable len!')
                if dlen <= 4:
                    return 0
                plen = cls.get_var_len_buffer(self.rfifo)

            print(plen)
            if plen > dlen:
                return 0
            
            pkt = cls(self.rfifo[:plen])
            print(pkt.get_data(as_string=True))
            if pkt.parse(self):
                self.eof = True

            self.rfifo = self.rfifo[plen:]
        return 0

    def send_packet(self, packet, pack=True):
        data = packet.get_data(pack=pack)
        print('Sending packet!')
        print(packet.get_data(as_string=True, pack=False))
        self.wfifo.extend(data)


    def do_sockets(self):
        print('Doing sockets')
        if self.eof:
            self.close()
        
        self.send_from_fifo()
        rfd, _, _ = select.select([self.sock], [], [], 0)

        for fd in rfd:
            if fd == self.sock:
                self.recv_to_fifo()
        
        self.send_from_fifo()

        self.parse_fifo()
        print('Done sockets')