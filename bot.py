import discord
import asyncio
from config import *
from socket_data import socket_data
from packets import dz_msg_to_channel, dz_connect
import time

client = discord.Client()
sd = socket_data(client, channels)
sd.connect()

login_pkt = dz_connect()
login_pkt.set_username(server_username)
login_pkt.set_password(server_password)
login_pkt.set_ip(server_ip)
login_pkt.set_port(server_port)
sd.send_packet(login_pkt)

while sd.state == sd.STATE_CONNECTING:
    print('attempting connection!')
    sd.do_sockets()
    time.sleep(1)


async def check_sockets():
    await client.wait_until_ready()
    while not client.is_closed():
        print('checking sockets')
        sd.do_sockets()
        for ch in sd.channels:
            print('checking channel')
            chn = client.get_channel(ch['id'])
            print(ch)
            for m in ch['messages']:
                print(m)
                await chn.send(m)
            ch['messages'] = []
        print('checked sockets')
        await asyncio.sleep(.3)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    for ch in channels:
        if message.channel.id == ch['id']:
            pkt = dz_msg_to_channel()
            pkt.set_channel(ch['name'])
            pkt.set_message(message.content)
            pkt.set_username(message.author.name, message.author.discriminator)
            sd.send_packet(pkt)
            break


client.bg_task = client.loop.create_task(check_sockets())
client.run(client_token)