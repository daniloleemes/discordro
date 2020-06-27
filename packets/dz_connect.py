import struct
import socket
from packets import DZPacket


class dz_connect(DZPacket):
    fmt = '<H24s24slh'
    header = 0x260f
    
    def __init__(self):
        self.username = None
        self.password = None
        self.ip = None
        self.port = None


    def pack(self):
        self.data = struct.pack(self.fmt, self.header, self.username, self.password, self.ip, self.port)
        return self.data
    
    def set_username(self, username):
        username = username.encode('ascii')
        if len(username) > 23:
            raise RuntimeError('Username must be no more than 23 characters')
        self.username = username
    
    def set_password(self, password):
        password = password.encode('ascii')
        if len(password) > 23:
            raise RuntimeError('Password must be no more than 23 characters')
        self.password = password
    
    def set_ip(self, ip=None):
        if not ip:
            ip = socket.gethostbyname(socket.gethostname())
        self.ip = struct.unpack("<I", socket.inet_aton(ip))[0]
        print(self.ip)
    
    def set_port(self, port):
        self.port = port