from struct import *
from collections import namedtuple

STRUCT_FORMAT = '!b10s25s'
comunicationPacket = namedtuple('Packet', 'type name message')

def buildPacket(type, name, message):
   packet = pack(STRUCT_FORMAT, type, name.encode('utf-8'), message.encode('utf-8'))
   return packet

def unpackPacket(record):
    packet = comunicationPacket._make(unpack(STRUCT_FORMAT, record))
    return (packet.type,
            packet.name.decode('utf-8', 'ignore').strip('\x00'),
            packet.message.decode('utf-8', 'ignore').strip('\x00'))