import sys
import socket
import socketserver


class Server:
    prompt = "HOST"
    info = None

    def __init__(self, _info) -> None:
        self.info = _info
        Server.info = _info
        Server.prompt = self.info.host_name

    def run(self):
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
        self.info = Server.info
        self.response = ''

        run, msg = True, ""
        while run:
            try:
                if len(self.response) > 0 and self.info.port_server == original_port: # Caso o nó solicitante seja o detentor
                    print(f"Resposta recebida: {self.response}")
                    
                self.data = self.request.recv(1024).strip()
                msg = self.data.decode("utf-8")

                # Evitar loop ao reprocessar mensagens de resposta
                if "resposta" in msg:
                    print(f"Resposta recebida: {msg}")
                    # self.request.sendall(self.data)

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
                self.response = response
                s.sendall(response.encode("utf-8"))
        except IOError as e:
            print(f"Erro ao enviar resposta ao solicitante original: {e}")
