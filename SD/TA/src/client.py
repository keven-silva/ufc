import socket


class Client:
    def __init__(self, info):
        self.sc = socket.socket()
        self.info = info
        self.connected = False
        self.prompt = "Digite a chave que deseja encontrar o detentor :>> "

    def run(self):
        self.open()
        while True:
            try:
                msg = int(input(self.prompt).strip())
                if msg:
                    self.send_query(msg)
                    response = self.receive()
                    if response:
                        self.process_response(response)

            except TypeError:
                if str(msg).lower() == "exit":
                    break

    def send(self, msg):
        if self.connected:
            self.sc.sendall(msg.encode("utf-8"))

    def receive(self):
        if self.connected:
            rec_msg = self.sc.recv(1024).strip()
            rec_msg = rec_msg.decode("utf-8")
            print(f"SUCESSOR({self.info.sucessor_name}):>> {rec_msg}")
            return rec_msg

    def send_query(self, key: int, command="detentor"):
        """Envia uma mensagem ao sucessor perguntando quem é o detentor da chave `key`."""
        if self.connected:
            query = f"[{key}, '{self.info.host_server}', {self.info.port_server}, '{command}']"
            self.send(query)

    def process_response(self, response):
        """Processa a resposta recebida e exibe quem é o detentor da chave."""
        if response.startswith("[") and response.endswith("]"):
            key, detentor_ip, detentor_port, _ = eval(response)
            print(
                f"\nO detentor da chave {key} é o nó com IP {detentor_ip} e porta {detentor_port}.\n"
            )

    def close(self):
        self.open()
        self.send("Exit")
        self.receive()

    def open(self):
        if not self.connected:
            try:
                self.sc.connect((self.info.host_server, self.info.sucessor))
                self.connected = True
            except IOError:
                print(
                    "SUCESSOR({0}), Host({1}), PORTA({2}) Falhou!".format(
                        self.info.sucessor_name,
                        self.info.host_server,
                        self.info.sucessor,
                    )
                )
                self.connected = False
