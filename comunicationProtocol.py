from struct import *
from ethernetUtils import *
from enum import Enum
from packetUtils import buildEthernet, buildPacket, unpackPacket, unpackEthernet
from threading import Thread
import time

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
        
    def sendPack(self, destinationMac = BROADCAST_MAC, komiPacket = b''):
        ethernet = buildEthernet(
            getMacAsByteArray(destinationMac), 
            getMacAsByteArray(self.macAddress),
            PROTOCOL_NUMBER)
            
        sendeth(ethernet + komiPacket, self.interface)
        # print("send %s type for %s" % (type.name.rjust(10), destinationMac))
    
    def startKomunication(self, heartbeat):
        self.sendPack(komiPacket= buildPacket(KOMI_Types.START.value, self.machineName))
        
        heartbeatThread = Thread(target=self.keepHeartbeat, args=[heartbeat], daemon=True)
        sniffThread = Thread(target=self.sniffNetwork, daemon=True)
        heartbeatThread.start()
        sniffThread.start()
        while True:
            pass
        
    def keepHeartbeat(self, delay):
        while True:
            time.sleep(delay)
            self.sendPack(komiPacket= buildPacket(KOMI_Types.HEARTBEAT.value, self.machineName))   

    def sniffNetwork(self):
        
        while True:
            rawSocket = getSniffingSocket(self.interface)
            packet =  rawSocket.recvfrom(50)
            
            ethernetPacket = unpackEthernet(packet[0][0:14])

            if ethernetPacket.ethType != PROTOCOL_NUMBER:
                rawSocket.close()
                continue
            
            komiPacket = unpackPacket(packet[0][14:50])
            
            rawSocket.close()



    def __handleStart(self, ethHeader, packet):
        print(packet)
        
    def __handleHeartBeat(self, ethHeader, packet):
        print(packet)
        
    def __handleTalk(self, ethHeader, packet):
        print(packet)
    
    availableHandlers = {
        KOMI_Types.START.value : __handleStart,
        KOMI_Types.HEARTBEAT.value : __handleHeartBeat,
        KOMI_Types.TALK.value : __handleTalk
        
    }
