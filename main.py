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
        print('Digite 1 para enviar mensagem, 2 para ver lista de enderecos ou 0 para sair')
        try:
            option = int(input('Opcao : '), 10)
        except KeyboardInterrupt:
            quit()
        except:
            option = None
            print("Valor digitado invalido. Favor inserir um numero de 0 a 2")

        if option == 1:
            try:
                macDst = input('Favor inserir endereco mac do remetente : ')
                message = input('Favor inserir mensagem a ser enviada : ')

                komi.komunicate(macDst, message)
            except KeyboardInterrupt:
                quit()
            except:
                print(
                    "Favor inserir um endereco mac no formato valido: XX:XX:XX:XX:XX:XX")

        if option == 2:
            komi.showAddressList()

        if option == 0:
            quit()
