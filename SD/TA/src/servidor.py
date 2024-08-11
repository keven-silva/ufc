import socketserver
import sys


class Servidor:
    prompt = "HOST"

    def __init__(self, info):
        self.info = info
        Servidor.prompt = self.info.host_name

    def run(self):
        with socketserver.TCPServer((self.info.HOST_SERVER, self.info.PORT_SERVER), ComunicadorTCPHandler) as server:
            try:
                server.serve_forever()
            finally:
                server.shutdown()


class ComunicadorTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        run = True
        while run:
            try:
                self.data = self.request.recv(1024).strip()
                msg = self.data.decode('utf-8')
                print(f"PEER: {self.client_address[0]}, Mensagem: {
                      msg}\n{Servidor.prompt} >> ", end="")
                self.request.sendall(self.data.upper())
            except:
                print("******************** CONNECTION DOWN *********************")
                sys.exit()

            if msg.lower().strip() == "exit":
                print(f"Antecessor({Servidor.prompt}) saiu (e informou)!!!")
                sys.exit()
