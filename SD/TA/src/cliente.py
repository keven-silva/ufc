import socket


class Cliente:
    def __init__(self, info):
        self.sc = socket.socket()
        self.info = info
        self.connected = False
        self.prompt = f"{self.info.host_server} >> "

    def run(self):
        self.open()
        while True:
            msg = input(self.prompt).strip()
            if msg:
                self.send(msg)
                self.receive()
            if msg.lower() == "exit":
                break

    def send(self, msg):
        if self.connected:
            self.sc.sendall(msg.encode("utf-8"))

    def receive(self):
        if self.connected:
            rec_msg = self.sc.recv(1024).strip()
            rec_msg = rec_msg.decode("utf-8")
            print(f"SUCESSOR({self.info.sucessor_name}) >> {rec_msg}")

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
                    "SUCESSOR({}), Host({}), PORTA({}) Falhou!".format(
                        self.info.sucessor_name,
                        self.info.host_server,
                        self.info.sucessor,
                    )
                )
                self.connected = False
