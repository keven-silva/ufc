import sys
import threading
from time import sleep

import readchar

from src.client import Client
from src.data_com import DataCom
from src.server import Server


def main():
    numero_de_pares = 2
    chave = None
    numero_de_pares = int(sys.argv[1]) if len(sys.argv) >= 2 else numero_de_pares
    info = DataCom("portas.txt", numero_de_pares)
    servidor = Server(info)
    cliente = Client(info)

    tserver = threading.Thread(target=servidor.run)
    tserver.start()

    sleep(0.1)

    print(info)
    print("***************** [<<ENTER>>=CONECTAR] ******************")

    key = readchar.readkey()
    if key in ["\r", "\n"]:
        print("****************** [<<EXIT>>=SAIR] *********************")
        tclient = threading.Thread(target=cliente.run)
        tclient.start()

        tclient.join()
        tserver.join()
    else:
        print("************ ABORT ANTES DE CONECTAR ********************")
        cliente.close()

    print(repr(readchar.readkey()))


if __name__ == "__main__":
    main()
