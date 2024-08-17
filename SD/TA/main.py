import sys
import threading
from time import sleep

import readchar

from src.cliente import Cliente
from src.data_com import DataCom
from src.servidor import Servidor


def main():
    numero_de_pares = 2
    chave = None
    numero_de_pares = int(sys.argv[1]) if len(sys.argv) >= 2 else numero_de_pares
    chave = int(sys.argv[2]) if len(sys.argv) >= 3 else None

    info = DataCom("portas.txt", numero_de_pares)
    servidor = Servidor(info)
    cliente = Cliente(info)

    tserver = threading.Thread(target=servidor.run)
    tserver.start()

    sleep(0.1)  # Melhora a precisão do tempo de espera

    print(info)
    print("***************** [<<ENTER>>=CONECTAR] ******************")

    enter = readchar.readkey() in ["\r", "\n"]
    if enter:
        print("****************** [<<EXIT>>=SAIR] *********************")
        tclient = threading.Thread(target=cliente.run)
        tclient.start()

        if chave is not None:
            resultado = cliente.send_query(chave)
            print(f"Resposta para chave {chave}: {resultado}")

        tclient.join()
        tserver.join()

        print("************* FIM CONECTADO ****************************")
    else:
        print("************ ABORT ANTES DE CONECTAR ********************")
        cliente.close()

    print(repr(readchar.readkey()))


if __name__ == "__main__":
    main()
