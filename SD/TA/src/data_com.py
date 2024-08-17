import sys


class DataCom:
    """Classe para gerenciar a comunicação em uma rede P2P."""

    SHOST = "localhost"
    SPORT = 3000
    FAIXA = 100

    def __init__(self, filename, num_pairs=1) -> None:
        """Inicializa um objeto DataCom.

        Args:
            filename: Nome do arquivo de configuração das portas.
            num_pairs: Número de pares na rede.
        """
        self.size = max(num_pairs, 1)
        self.map = []

        for i in range(self.size):
            server_port, client_port = i, (i + 1)
            if client_port < self.size:
                self.map.append([server_port, client_port])
            else:
                self.map.append([server_port, 0])
        self.idx_map = self._config_ports(filename)

    def _config_ports(self, filename):
        """Lê e grava as portas do arquivo de configuração.

        Args:
            filename: Nome do arquivo de configuração.
        """
        _port = -1
        try:
            with open(filename, "r") as f:
                _port = int(f.read())

            with open(filename, "w") as f:
                f.write(str(_port + 1))
        except IOError:
            print("Erro ao ler/gravar arquivo de configuração!")
            sys.exit(1)

        rest_of_division = _port % self.size
        self.host_server = DataCom.SHOST
        self.port_server = self.map[rest_of_division][0] * DataCom.FAIXA + DataCom.SPORT
        self.sucessor = self.map[rest_of_division][1] * DataCom.FAIXA + DataCom.SPORT
        self.sucessor_name = f"NO{self.port_server}"
        # DE ACORDO COM O DO PROFESSOR, A LINHA A CIMA DEVERIA SER A LINHA ABAIXO.
        # self.sucessor_name = f"NO{self.sucessor}"

        # DE ACORDO COM O DO PROFESSOR, DEVERIA TER A LINHA ABAIXO.
        # self.host_name = f"NO{self.port_server}"

        # DE ACORDO COM O DO PROFESSOR, DEVERIA SER if rest_of_division -1 >= 0. NOTE A ADIÇÃO DO -1.
        ant_i = rest_of_division - 1 if rest_of_division >= 0 else self.size - 1
        self.antecessor_name = f"NO{self.map[ant_i][0] * DataCom.FAIXA + DataCom.SPORT}"
        self.set_f(rest_of_division)
        return rest_of_division

    def __repr__(self):
        """Retorna uma representação em string do objeto."""
        s = f"""Servidor({self.host_server}), PortServer({self.port_server}), SUCESSO({
            self.sucessor}), -> FAIXA [{self.fi}-{self.fj}] ...\n"""
        return f"""{s}\nCliente vais conectar assim: ESCUTA({self.host_server}), SUCESSOR({self.sucessor}) OK!"""

    def set_f(self, i: int):
        """Configura os valores de Fi e Fj.

        Args:
            i: Índice do nó.
        """
        self.fi = int(self.sucessor - DataCom.SPORT - DataCom.FAIXA + 1)
        self.fj = int(self.sucessor - DataCom.SPORT)
        # Se for o último nó
        if i == self.size - 1:
            self.fi = int(self.port_server - DataCom.SPORT + 1)
            self.fj = DataCom.FAIXA * self.size
