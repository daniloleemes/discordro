import struct
import socket
import string
from . import DZPacket

printable = set(string.printable)


def rem_uni(s):
    """Remove unprintable characters"""
    return ''.join(filter(lambda x: x in printable, s))


class dz_msg_to_channel(DZPacket):
    header = 0xe03
    fmt = '<HH20s24s%ss'
    fmt_len = -1

    def __init__(self):
        self.pkt_len = None
        self.channel = None
        self.username = None
        self.message = None
        self.my_fmt = None

    def pack(self):
        self.pkt_len = 2 + 2 + 20 + 24 + len(self.message) + 1
        self.my_fmt = self.fmt % (len(self.message) + 1)
        self.data = struct.pack(
            self.my_fmt, self.header, self.pkt_len, self.channel, self.username, self.message)
        return self.data

    def set_username(self, username, discriminator):
        username = rem_uni(username).encode('ascii')
        discriminator = discriminator.encode('ascii')

        # truncate username to 18
        username = username[:18] + '#'.encode('ascii') + discriminator
        if len(username) > 23:
            raise RuntimeError('Username must be no more than 23 characters')
        self.username = username

    def set_message(self, message):
        message = rem_uni(message).encode('ascii')
        if len(message) > 254:
            raise RuntimeError('Message must be no more than 254 characters')
        self.message = message

    def set_channel(self, channel):
        channel = rem_uni(channel).encode('ascii')
        if len(channel) > 19:
            raise RuntimeError('Channel must be no more than 19 characters')
        self.channel = channel
