import sys
import socket
import socketserver


class Server(socketserver.ThreadingMixIn, socketserver.TCPServer):
    prompt = "HOST"

    def __init__(self, _info) -> None:
        self.info = _info
        Server.prompt = self.info.host_name
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
        while True:
            try:
                self.data = self.request.recv(1024).strip()
                msg = self.data.decode("utf-8")
                # print(
                #     "PEER: {0}, Mensagem:\n{1}\n{2} >> ".format(
                #         self.client_address[0],
                #         msg,
                #         Server.prompt,
                #     ),
                #     end="",
                # )

                # Evitar loop ao reprocessar mensagens de resposta
                if "resposta" in msg:
                    print(f"Resposta recebida: {msg}")
                    return self.request.sendall(self.data.upper())

                # Processa a mensagem recebida
                if msg.startswith("[") and msg.endswith("]"):
                    key, original_ip, original_port, command = eval(msg)
                    if command == "detentor":
                        if self.is_responsible_for_key(key):
                            # Se o nó atual for o detentor da chave, responde ao solicitante original
                            peer_response = f"[{key}, '{self.info.host_server}', {self.info.port_server}, 'resposta']"
                            self.send_response_to_origin(
                                peer_response, original_ip, original_port
                            )
                        else:
                            # Se não for, use a Finger Table para encontrar o sucessor mais próximo
                            successor, successor_name = self.info.find_successor(key)
                            self.forward_request_to_successor(
                                key, original_ip, original_port, command, successor
                            )
                    else:
                        self.request.sendall(self.data.upper())
                else:
                    self.request.sendall(self.data.upper())

            except Exception as e:
                print("******************** CONNECTION DOWN *********************")
                print(f"Error: {e}")
                sys.exit()

            if str(msg).lower().strip() == "exit":
                print(f"Antecessor({0}) saiu (e informou)!!!".format(Server.prompt))
                sys.exit()

    def is_responsible_for_key(self, key):
        """Verifica se o nó atual é responsável pela chave `key`."""
        if self.info.fi > self.info.fj:
            return self.info.fi <= key
        else:
            return self.info.fi <= key <= self.info.fj

    def forward_request_to_successor(
        self, key, original_ip, original_port, command, successor
    ):
        """Encaminha a solicitação para o sucessor."""
        try:
            with socket.socket() as s:
                s.connect((self.info.host_server, successor))
                query = f"[{key}, '{original_ip}', {original_port}, '{command}']"
                s.sendall(query.encode("utf-8"))

                # Aguarda a resposta do sucessor e a retorna ao solicitante original
                response = s.recv(1024).strip().decode("utf-8")
                self.send_response_to_origin(response, original_ip, original_port)
        except IOError as e:
            print(f"Erro ao encaminhar a solicitação para o sucessor: {e}")

    def send_response_to_origin(self, response, original_ip, original_port):
        """Envia a resposta diretamente ao solicitante original."""
        try:
            with socket.socket() as s:
                s.connect((original_ip, original_port))
                s.sendall(response.encode("utf-8"))
        except IOError as e:
            print(f"Erro ao enviar resposta ao solicitante original: {e}")
