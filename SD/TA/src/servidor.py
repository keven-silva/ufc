import sys
import socketserver


class Servidor(socketserver.ThreadingMixIn, socketserver.TCPServer):
    prompt = "HOST"

    def __init__(self, _info) -> None:
        self.info = _info
        Servidor.prompt = self.info.host_name
        # Passa a info para o ComunicadorTCPHandler via um lambda
        handler = lambda *args, **kwargs: ComunicadorTCPHandler(self.info, *args, **kwargs)
        super().__init__((self.info.host_server, self.info.port_server), handler)


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
                        # Simulate the lookup for the key owner
                        peer_response = f"[{key}, '{ip}', {port}, 'detentor']"
                        print(f"\nO detentor da chave {key} é o nó {self.info.host_name} com a porta {self.info.port_server}\n")
                        
                        self.request.sendall(peer_response.encode("utf-8"))
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

    # def process_message(self, msg):
    #     """Processa a mensagem recebida e decide se redireciona ou responde diretamente."""
    #     try:
    #         parts = eval(msg)
    #         key = int(parts[0])
    #         command = parts[3].lower()

    #         if self.is_responsible(key):
    #             if command == "detentor":
    #                 return f"Chave {key} encontrada no nó {self.server.info.host_server}:{self.server.info.port_server}"
    #             else:
    #                 return f"Comando '{command}' não reconhecido para a chave {key}."
    #         else:
    #             successor, successor_name = self.server.info.find_successor(key)
    #             print(
    #                 f"Redirecionando a chave {key} para {successor_name} ({successor})"
    #             )
    #             return f"Redirecionando para {successor_name} ({successor})"
    #     except Exception as e:
    #         return f"Erro ao processar mensagem: {str(e)}"

    # def is_responsible(self, key):
    #     """Verifica se o nó atual é responsável pela chave `key`."""
    #     return self.info.fi <= key <= self.info.fj
