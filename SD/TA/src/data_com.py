import sys
import math


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
        self.finger_table = []

        for a in range(self.size):
            server_port, client_port = a, (a + 1)
            if client_port < self.size:
                self.map.append([server_port, client_port])
            else:
                self.map.append([server_port, 0])
        self.idx_map = self.__config_ports(filename)
        self.__calculate_finger_table()

    def __config_ports(self, filename):
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
        self.sucessor_name = f"NO[{self.sucessor}]"
        self.host_name = f"NO[{self.port_server}]"

        ant_i = rest_of_division - 1 if rest_of_division - 1 >= 0 else self.size - 1
        self.antecessor_name = (
            f"NO[{self.map[ant_i][0] * DataCom.FAIXA + DataCom.SPORT}]"
        )
        self.set_f(rest_of_division)
        return rest_of_division

    def __calculate_finger_table(self):
        """Calcula a tabela de 'finger' para o nó atual."""
        m = self.size  # Número de nós
        
        current_node = self.port_server # Ex: 3120
        current_node_str = str(current_node)[1:]  # '120'
        current_node_modified = int(current_node_str) # 120

        for i in range(m):
            if self.idx_map == i:
                print(f"Finger Table ({current_node_modified}):")
                
                j = 0
                while current_node_modified + 2**j < m * DataCom.FAIXA:
                    calcCurrentLine = current_node_modified + 2**j
                    responsavel = 0
                    
                    while calcCurrentLine > responsavel:
                        responsavel += DataCom.FAIXA
                        
                    # if responsavel == m * DataCom.FAIXA: # Se o NO for responsável pelos seus antecessores
                    #     responsavel = 0
                    
                    responsavel-= DataCom.FAIXA # Se o NO for responsável pelos seus sucessores
                    
                    print(f"{current_node_modified} + 2^{j} = {calcCurrentLine} => {responsavel}")
                    
                    j += 1
                    
    def find_successor(self, key):
        """Encontra o nó sucessor responsável pela chave `key`."""
        # Verifica se o nó atual é responsável pela chave
        if self.fi <= key <= self.fj:
            return self.port_server, self.host_name

        # Busca na Finger Table
        for entry in reversed(self.finger_table):
            if entry["start"] <= key < self.sucessor:
                return entry["successor"], entry["successor_name"]

        # Se a Finger Table não contém um sucessor adequado, encaminha para o sucessor direto
        return self.sucessor, self.sucessor_name

    def __repr__(self):
        """Retorna uma representação em string do objeto."""
        s = "Servidor({0}), PortServer({1}), SUCESSOR({2}), -> FAIXA [{3}-{4}] ...\n".format(
            self.host_server,
            self.port_server,
            self.sucessor,
            self.fi,
            self.fj,
        )

        ft_str = "\n".join(
            [
                f"start: {entry['start']}, successor: {entry['successor_name']}"
                for entry in self.finger_table
            ]
        )
        return (
            s
            + "\nCliente vais conectar assim: ESCUTA({0}), SUCESSOR({1}) OK!\n{2}".format(
                self.host_name,
                self.sucessor_name,
                ft_str,
            )
        )

    def set_f(self, i: int):
        """Configura os valores de Fi e Fj.

        Args:
            i: Índice do nó.
        """
        self.fi = int(self.sucessor - DataCom.SPORT - DataCom.FAIXA + 1)
        self.fj = int(self.sucessor - DataCom.SPORT)
        # Se for o último nó
        if i + 1 == self.size:
            self.fi = int(self.port_server - DataCom.SPORT + 1)
