import socketserver
import sys


class Servidor:
    prompt = "HOST"

    def __init__(self, info) -> None:
        self.info = info
        # DE ACORDO COM O DO PROFESSOR, DEVERIA SER self.info.host_name.
        Servidor.prompt = self.info.host_server

    def run(self) -> None:
        with socketserver.TCPServer(
            (self.info.host_server, self.info.port_server),
            ComunicadorTCPHandler,
        ) as server:
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
                msg = self.data.decode("utf-8")
                print(
                    f"PEER: {self.client_address[0]}, Mensagem:\n{msg}\n{Servidor.prompt} >> ",
                    end="",
                )

                # Parse the received message
                if msg.startswith("[") and msg.endswith("]"):
                    key, ip, port, command = eval(msg)
                    if command == "detentor":
                        # Simulate the lookup for the key owner
                        peer_response = f"[{key}, '{ip}', {port}, 'NÓ (responsável)']"
                        self.request.sendall(peer_response.encode("utf-8"))
                    else:
                        self.request.sendall(self.data.upper())
                else:
                    self.request.sendall(self.data.upper())

            except Exception as e:
                print("******************** CONNECTION DOWN *********************")
                print(f"Error: {e}")
                sys.exit()

            if msg.lower().strip() == "exit":
                print(f"Antecessor({Servidor.prompt}) saiu (e informou)!!!")
                sys.exit()
