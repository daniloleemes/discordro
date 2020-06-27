import struct
import socket
from . import ZDPacket

class zd_connect_ack(ZDPacket):
    header = 0xe02
    fmt = '<Hb'
    
    def __init__(self, data):
        self.err_code = None
        self.data = data
        self.unpack()
    
    def unpack(self):
        _, self.err_code = struct.unpack(self.fmt, self.data)

    def parse(self, sd):
        if self.err_code:
            sd.state = sd.STATE_DISCONNECTED
            print(f'Server rejected connection! Bad!')
            return 1
        else:
            sd.state = sd.STATE_CONNECTED
            print(f'Server accepted connection! Good!')
            return 0
