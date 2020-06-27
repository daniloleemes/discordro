from abc import ABC, abstractmethod
from binascii import hexlify
import struct

class Packet(ABC):
    header = None
    fmt = None
    fmt_len = None

    def __init__(self):
        self.data = None
    
    def get_header(self, *, as_string=False):
        if as_string:
            return format(self.header, '#06x')
        return self.header
    
    @classmethod
    def parse_header(cls, buffer):
        return struct.unpack('<H', buffer)[0]

    def get_data(self, *, as_string=False):
        if as_string:
            return self.data_str(self.data)
        return self.data

    @classmethod
    def get_var_len_buffer(self, buffer):
        return struct.unpack('<HH', buffer[:4])[1]

    def get_var_len(self):
        return self.get_var_len_buffer(self.data)


    @staticmethod
    def iscntrl(c):
        #c = ord(c)
        if (c >= 0 and c <= 0x1f) or c == 0x7f:
            return True
        return False

    @staticmethod
    def data_str(buffer):
        i = 0
        s = ''
        s += '    00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F    0123456789ABCDEF\n'
        asc = ''
        buf = ''
        for i in range(len(buffer)):
            
            c = buffer[i]
            asc += '.' if Packet.iscntrl(c) else str(chr(c))
            buf += '%02X ' % c
            if (i % 16) == 15:
                s += ('%03X %s   %s' % (i // 16, buf, asc)) + '\n'
                asc = ''
                buf = ''
        if i % 16 != 0:
            s += ('%03X %-48s   %-16s' % ( i // 16, buf, asc)) + '\n'
        return s



class DZPacket(Packet):
    @abstractmethod
    def pack(self):
        pass

    def get_data(self, *, as_string=False, pack=True):
        if pack:
            self.pack()
        if as_string:
            return self.data_str(self.data)
        return self.data

class ZDPacket(Packet):
    @abstractmethod
    def unpack(self):
        pass

    @abstractmethod
    def parse(self, sd):
        pass

    def get_data(self, *, as_string=False):
        if as_string:
            return self.data_str(self.data)
        return self.data

    @classmethod
    def get_fmt_len(self):
        if self.fmt_len == -1:
            return self.fmt_len
        return struct.calcsize(self.fmt)