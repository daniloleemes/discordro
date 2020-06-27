from . import *


dz_packet_dict = {
    dz_connect.header: dz_connect,
    dz_msg_to_channel.header: dz_msg_to_channel
}

zd_packet_dict = {
    zd_connect_ack.header: zd_connect_ack,
    zd_msg_to_discord.header: zd_msg_to_discord,
}