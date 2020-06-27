import struct
import socket
from . import ZDPacket

class zd_msg_to_discord(ZDPacket):
    header = 0xe04
    fmt = '<HH20s%ds'
    fmt_len = -1

    def __init__(self, data):
        self.channel = None
        self.message = None
        self.data = data
        self.my_fmt = self.fmt % (self.get_var_len_buffer(data) - 24)
        print(self.my_fmt)
        self.unpack()
    
    def unpack(self):
        _, _, self.channel, self.message = struct.unpack(self.my_fmt, self.data)
        self.channel = self.channel.split(b'\0',1)[0].decode('utf8')
        self.message = self.message.split(b'\0',1)[0].decode('utf8')

    def parse(self, sd):
        if not self.channel:
            print('No channel?')
            return 1
        if not self.message:
            print('No message?')
            return 1

        print(f'Good packet! Channel: [{self.channel}] | Message:')
        print(self.message)
        for ch in sd.channels:
            print(ch)
            if ch['name'] == self.channel:
                print('they\'re the same!')
                ch['messages'].append(self.message)
                print(ch)
                #sd.client.get_channel(ch['id']).send(self.message)
                break

