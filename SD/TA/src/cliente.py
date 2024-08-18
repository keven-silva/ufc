import socket


class Cliente:
    def __init__(self, info):
        self.sc = socket.socket()
        self.info = info
        self.connected = False
        self.prompt = f"{self.info.host_server} :>> "

    def run(self):
        self.open()
        while True:
            msg = input(self.prompt).strip()
            if msg:
                self.send(msg)
                self.receive()
            if str(msg).lower() == "exit":
                break

    def run_detentor(self):
        self.open()
        while True:
            key = int(input("Digite a chave que deseja encontrar o detentor: ").strip())
            if key == -1:
                break
            if key:
                self.send_query(key)
                response = self.receive()
                if response:
                    print(f"Detentor da chave {key}: {response}")

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

            response = self.receive()
            return response

    # def extract_new_successor_info(self, response):
    #     """Extrai as informações do próximo nó a partir da resposta de redirecionamento."""
    #     try:
    #         parts = response.split()
    #         successor_name = parts[2]
    #         successor_port = int(parts[-1].strip("()"))
    #         return {"successor_name": successor_name, "successor": successor_port}
    #     except Exception as e:
    #         raise ValueError(f"Erro ao extrair informações do redirecionamento: {e}")

    # def open_to_new_successor(self, new_succ_info):
    #     """Abre uma nova conexão com o próximo sucessor."""
    #     self.sc.close()
    #     self.sc = socket.socket()
    #     self.connected = False
    #     try:
    #         self.sc.connect((self.info.host_server, new_succ_info["successor"]))
    #         self.connected = True
    #     except IOError:
    #         print(
    #             f"Falhou ao conectar com o novo sucessor {new_succ_info['successor_name']} ({new_succ_info['successor']})"
    #         )

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
