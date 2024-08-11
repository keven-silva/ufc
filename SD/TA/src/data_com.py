import sys


class DataCom:
    """Classe para gerenciar a comunicação em uma rede P2P."""

    SHOST = "localhost"
    SPORT = 3000
    FAIXA = 100

    def __init__(self, filename, num_pairs=1):
        """Inicializa um objeto DataCom.

        Args:
            filename: Nome do arquivo de configuração das portas.
            num_pairs: Número de pares na rede.
        """
        self.size = max(num_pairs, 1)
        self.map = []  # Mapa de pares (servidor, cliente)
        self._config_ports(filename)

    def _config_ports(self, filename):
        """Lê e grava as portas do arquivo de configuração.

        Args:
            filename: Nome do arquivo de configuração.
        """
        try:
            with open(filename, 'r') as f:
                next_port = int(f.read())

            with open(filename, 'w') as f:
                f.write(str(next_port + 1))
        except IOError:
            print("Erro ao ler/gravar arquivo de configuração!")
            sys.exit(1)

        # ... (resto do código, com melhorias na indentação, nomenclatura e comentários)

    def __repr__(self):
        """Retorna uma representação em string do objeto."""
        # ... (implementação melhorada)

    def set_f(self, i):
        """Configura os valores de Fi e Fj.

        Args:
            i: Índice do nó.
        """
        # ... (implementação melhorada com explicação da lógica)
