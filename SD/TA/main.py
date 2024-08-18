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
    info = DataCom("portas.txt", numero_de_pares)
    servidor = Servidor(info)
    cliente = Cliente(info)

    tserver = threading.Thread(target=servidor.run)
    tserver.start()

    sleep(0.1)

    print(info)
    print("***************** [<<ENTER>>=CONECTAR] ******************")
    print("***************** [<<D>>=DETECTAR] **********************")

    key = readchar.readkey() 
    if key in ["\r", "\n"]:
        print("****************** [<<EXIT>>=SAIR] *********************")
        tclient = threading.Thread(target=cliente.run)
        tclient.start()
        
        tclient.join()
        tserver.join()
        
    elif key.lower() == 'd':
        # Novo código: Permitir que o usuário digite a chave a ser detectada
        print("****************** [<<-1>>=SAIR] *********************")
        tclient2 = threading.Thread(target=cliente.run_detentor)
        tclient2.start()

        tclient2.join()
        tserver.join()
        # Agora oferece uma nova escolha de ação ao usuário
        print("Escolha a próxima ação:")
        print("***************** [<<ENTER>>=CONECTAR] ******************")
        print("***************** [<<D>>=DETECTAR NOVAMENTE] **********************")

    else:
        print("************ ABORT ANTES DE CONECTAR ********************")
        cliente.close()

    print(repr(readchar.readkey()))


if __name__ == "__main__":
    main()
