from struct import *
from collections import namedtuple

KOMI_STRUCT_FORMAT = '!b10s25s'
ETH_STRUCT_FORMAT = '!6s6sH'
comunicationPacket = namedtuple('Comunication', 'type name message')
ethernetPacket = namedtuple('Ethernet', 'macAddr macDst ethType')


def buildPacket(type, name, message = ''):
   packet = pack(KOMI_STRUCT_FORMAT, type, name.encode('utf-8'), message.encode('utf-8'))
   return packet

def unpackPacket(record):
    packet = comunicationPacket._make(unpack(KOMI_STRUCT_FORMAT, record))
    return comunicationPacket._make([packet.type,
            packet.name.decode('utf-8', 'ignore').strip('\x00'),
            packet.message.decode('utf-8', 'ignore').strip('\x00')])
    
def buildEthernet(destinationMac, sourceMac, protocol):
   packet = pack(ETH_STRUCT_FORMAT, destinationMac, 
      sourceMac, protocol)
   return packet

def unpackEthernet(record):
   packet = ethernetPacket._make(unpack(ETH_STRUCT_FORMAT, record))
   return packet
