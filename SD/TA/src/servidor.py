import sys
import socketserver


class Servidor(socketserver.ThreadingMixIn, socketserver.TCPServer):
    prompt = "HOST"

    def __init__(self, info) -> None:
        self.info = info
        # DE ACORDO COM O DO PROFESSOR, DEVERIA SER self.info.host_name.
        Servidor.prompt = self.info.host_server
        super().__init__((info.host_server, info.port_server), ComunicadorTCPHandler)


class ComunicadorTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        run = True
        while run:
            try:
                self.data = self.request.recv(1024).strip()
                msg = self.data.decode("utf-8")
                print(
                    f"PEER: {self.client_address[0]}, Mensagem:\n{msg}\n{self.server.info.host_server} >> ",
                    end="",
                )

                # Redirecionamento de mensagens com base na chave
                response = self.process_message(msg)
                self.request.sendall(response.encode("utf-8"))

            except Exception as e:
                print("******************** CONNECTION DOWN *********************")
                print(f"Error: {e}")
                sys.exit()

            if msg.lower().strip() == "exit":
                print(
                    f"Antecessor({self.server.info.host_server}) saiu (e informou)!!!"
                )
                sys.exit()

    def process_message(self, msg):
        """Processa a mensagem recebida e decide se redireciona ou responde diretamente."""
        try:
            parts = eval(msg)
            key = int(parts[0])
            command = parts[3].lower()

            if self.is_responsible(key):
                if command == "detentor":
                    return f"Chave {key} encontrada no nó {self.server.info.host_server}:{self.server.info.port_server}"
                else:
                    return f"Comando '{command}' não reconhecido para a chave {key}."
            else:
                successor, successor_name = self.server.info.find_successor(key)
                print(
                    f"Redirecionando a chave {key} para {successor_name} ({successor})"
                )
                return f"Redirecionando para {successor_name} ({successor})"
        except Exception as e:
            return f"Erro ao processar mensagem: {str(e)}"

    def is_responsible(self, key):
        """Verifica se o nó atual é responsável pela chave `key`."""
        return self.server.info.fi <= key <= self.server.info.fj
