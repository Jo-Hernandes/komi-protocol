import socket as sock
from socket import AF_PACKET, SOCK_RAW
from struct import *

def sendeth(eth_frame, interface = "eth0"):
    """Send raw Ethernet packet on interface."""
    s = sock.socket(AF_PACKET, SOCK_RAW)
    s.bind((interface, 0))
    return s.send(eth_frame)
 
def getMacAsByteArray(readableMac):
    """returns the readable mac address as byteArray

    Args:
        readableMac (String): mac in format XX:XX:XX:XX:XX:XX

    Returns:
        byteArray : the mac as bytes
    """    
    return bytearray.fromhex(readableMac.translate(str.maketrans('','',':')))

def getReadableMac(byteArray):
    return "%02x:%02x:%02x:%02x:%02x:%02x" % unpack("BBBBBB",byteArray)

def getSniffingSocket(interface = "eth0"):
    s = sock.socket(sock.AF_PACKET, sock.SOCK_RAW, sock.htons(3))
    s.bind((interface, 0))

    return s
    