from struct import *
from ethernetUtils import *
from enum import Enum
from packetBuilder import buildPacket, unpackPacket
from threading import Thread
import time
import binascii

class KOMI_Types(Enum):
    START = 0
    HEARTBEAT = 1
    TALK = 2

BROADCAST_MAC = 'ff:ff:ff:ff:ff:ff'
PROTOCOL_NUMBER = 0x666

class KomiProto:
    def __init__(self, machineName, readableMacAddress, interface):
        self.machineName = machineName
        self.macAddress = readableMacAddress
        self.interface = interface
        
    def __str__(self):
        return 'Machine %s - Mac Address %s' % (self.machineName, self.macAddress)
        
    def sendPack(self, type : KOMI_Types, destinationMac = BROADCAST_MAC, message = ''):
        dst_mac = getMacAsByteArray(destinationMac)
        src_mac = getMacAsByteArray(self.macAddress)
    
        # Ethernet header
        eth_header = pack('!6B6BH', dst_mac[0], dst_mac[1], dst_mac[2], dst_mac[3], dst_mac[4], dst_mac[5], 
            src_mac[0], src_mac[1], src_mac[2], src_mac[3], src_mac[4], src_mac[5], PROTOCOL_NUMBER)
    
        # final full packet - syn packets dont have any data
        packet = eth_header  +  buildPacket(type.value, self.machineName, message)
        r = sendeth(packet, self.interface)
        print("send %s type for %s - message : %s" % (type.name.rjust(10), destinationMac, message))
    
    def startKomunication(self, heartbeat):
        self.sendPack(KOMI_Types.START)
        
        thread_a = Thread(target=self.keepHeartbeat, args=[heartbeat], daemon=True)
        thread_b = Thread(target=self.sniffNetwork, daemon=True)
        thread_a.start()
        thread_b.start()
        while True:
            pass
        
    def keepHeartbeat(self, delay):
        while True:
            time.sleep(delay)
            self.sendPack(KOMI_Types.HEARTBEAT)   

    def sniffNetwork(self):
        
        while True:
            rawSocket = getSniffingSocket(self.interface)
            packet =  rawSocket.recvfrom(2048)
            
            ethernet_header = packet[0][0:14]
            ethernet_detailed = unpack("!6s6s2s", ethernet_header)

            if ethernet_detailed[2] != PROTOCOL_NUMBER:
                rawSocket.close()
                continue

            print ("****************_ETHERNET_FRAME_****************")
            print ("Dest MAC:        ", getReadableMac(ethernet_detailed[0]))
            print ("Source MAC:      ", getReadableMac(ethernet_detailed[1]))
            print ("Type:            ", ethernet_detailed[2].hex())
            
            komi_packet = unpackPacket(packet[0][14:50])
            print(komi_packet)
            
            
            rawSocket.close()
