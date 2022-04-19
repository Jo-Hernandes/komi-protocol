from struct import *
from ethernetUtils import *
from enum import Enum
from packetUtils import buildEthernet, buildPacket, unpackPacket, unpackEthernet
from threading import Thread
from addressBook import AddressBook
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
        self.addressBook = AddressBook()

    def __str__(self):
        return 'Machine %s - Mac Address %s' % (self.machineName, self.macAddress)

    def sendPack(self, destinationMac=BROADCAST_MAC, komiPacket=None):
        ethernet = buildEthernet(
            getMacAsByteArray(self.macAddress),
            getMacAsByteArray(destinationMac),
            PROTOCOL_NUMBER)

        sendeth(ethernet + komiPacket, self.interface)

    def startKomunication(self, heartbeat):
        self.sendPack(komiPacket=buildPacket(
            KOMI_Types.START.value, self.machineName))

        heartbeatThread = Thread(target=self.keepHeartbeat,
                                 args=[heartbeat], daemon=True)
        sniffThread = Thread(target=self.sniffNetwork,
                             daemon=True)
        updateAddresses = Thread(target=self.addressBook.updateData,
                                 daemon=True)

        heartbeatThread.start()
        sniffThread.start()
        updateAddresses.start()

    def keepHeartbeat(self, delay):
        while True:
            time.sleep(delay)
            self.sendPack(komiPacket=buildPacket(
                KOMI_Types.HEARTBEAT.value, self.machineName))

    def komunicate(self, macDst, message=''):
        self.sendPack(
            destinationMac=macDst,
            komiPacket=buildPacket(
                KOMI_Types.TALK.value, self.machineName, message))

    def sniffNetwork(self):

        while True:
            rawSocket = getSniffingSocket(self.interface)
            packet = rawSocket.recvfrom(50)

            ethernetPacket = unpackEthernet(packet[0][0:14])

            if (ethernetPacket.ethType == PROTOCOL_NUMBER
                    and ethernetPacket.macAddr != self.macAddress):
                komiPacket = unpackPacket(packet[0][14:50])
                {
                    KOMI_Types.START.value: self.__handleStart,
                    KOMI_Types.HEARTBEAT.value: self.__handleHeartBeat,
                    KOMI_Types.TALK.value: self.__handleTalk
                }.get(komiPacket.type, (lambda: print("Komi Type inexistente")))(ethernetPacket, komiPacket)

            rawSocket.close()

    def __handleStart(self, ethHeader, packet):
        self.sendPack(destinationMac=ethHeader.macAddr,
                      komiPacket=buildPacket(KOMI_Types.HEARTBEAT.value, self.machineName))

    def __handleHeartBeat(self, ethHeader, packet):
        self.addressBook.includeItem(packet.name, ethHeader.macAddr)

    def __handleTalk(self, ethHeader, packet):
        print('Mensagem recebida de %s - %s : %s' %
              (packet.name, ethHeader.macAddr, packet.message))

    def showAddressList(self):
        self.addressBook.showData()
