from struct import *
from comunicationProtocol import *
import argparse


def getUserMacAddress(interface):
    return open('/sys/class/net/'+interface+'/address').read().splitlines()[0]


def setupArguments():
    parser = argparse.ArgumentParser(
        description='Program sends and receives Raw Sockets packages through the ethernet protocol')
    parser.add_argument(
        '-n', '--name', required=True, type=str, help='Name of the machine')
    parser.add_argument(
        '-i', '--interface', required=True, type=str, help='Ethernet interface')
    parser.add_argument(
        '-hb', '--heartbeat', required=False, type=int, help='Time between heartbeat packages', default=5)

    return parser.parse_args()


if __name__ == "__main__":
    args = setupArguments()
    mac = getUserMacAddress(args.interface)

    komi = KomiProto(args.name, mac, args.interface)
    print(komi)
    komi.startKomunication(args.heartbeat)
    while True:
        pass
