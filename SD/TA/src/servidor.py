import sys
import socket
import socketserver


class Servidor(socketserver.ThreadingMixIn, socketserver.TCPServer):
    prompt = "HOST"

    def __init__(self, _info) -> None:
        self.info = _info
        Servidor.prompt = self.info.host_name
        # Passa a info para o ComunicadorTCPHandler via um lambda
        handler = lambda *args, **kwargs: ComunicadorTCPHandler(
            self.info, *args, **kwargs
        )
        super().__init__((self.info.host_server, self.info.port_server), handler)

    def run(self):
        try:
            self.serve_forever()
        finally:
            self.shutdown()


class ComunicadorTCPHandler(socketserver.BaseRequestHandler):
    def __init__(self, info, *args, **kwargs):
        self.info = info  # Armazena a informação passada
        super().__init__(*args, **kwargs)  # Chama o construtor da superclasse

    def handle(self):

        run, msg = True, ""
        while run:
            try:
                self.data = self.request.recv(1024).strip()
                msg = self.data.decode("utf-8")
                print(
                    "PEER: {0}, Mensagem:\n{1}\n{2} >> ".format(
                        self.client_address[0],
                        msg,
                        Servidor.prompt,
                    ),
                    end="",
                )

                # Parse the received message
                if msg.startswith("[") and msg.endswith("]"):
                    key, ip, port, command = eval(msg)
                    if command == "detentor":
                        if self.is_responsible_for_key(key):
                            # Se o nó atual for o detentor da chave, responde ao solicitante
                            peer_response = f"[{key}, '{self.info.host_server}', {self.info.port_server}, 'detentor']"
                            self.request.sendall(peer_response.encode("utf-8"))
                        else:
                            # Se não for, encaminha a mensagem para o próximo sucessor
                            self.forward_request_to_successor(key, ip, port, command)

                    else:
                        self.request.sendall(self.data.upper())
                else:
                    self.request.sendall(self.data.upper())

            except Exception as e:
                print("******************** CONNECTION DOWN *********************")
                print(f"Error: {e}")
                sys.exit()

            if str(msg).lower().strip() == "exit":
                print(f"Antecessor({0}) saiu (e informou)!!!".format(Servidor.prompt))
                sys.exit()

    def is_responsible_for_key(self, key):
        """Verifica se o nó atual é responsável pela chave `key`."""
        return self.info.fi <= key <= self.info.fj

    def forward_request_to_successor(self, key, ip, port, command):
        """Encaminha a solicitação para o sucessor."""
        try:
            with socket.socket() as s:
                s.connect((self.info.host_server, self.info.sucessor))
                query = f"[{key}, '{ip}', {port}, '{command}']"
                s.sendall(query.encode("utf-8"))

                # Aguarda a resposta do sucessor
                response = s.recv(1024).strip().decode("utf-8")
                self.request.sendall(response.encode("utf-8"))
        except IOError as e:
            print(f"Erro ao encaminhar a solicitação para o sucessor: {e}")
