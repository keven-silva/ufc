# saved as Server.py
# Python Remote Objects (Pyro)
import Pyro4


@Pyro4.expose
class Aluno(object):  # Implementacao
    def getDisciplina(self):
        return "Sistemas Distribuidos!"


daemon = Pyro4.Daemon()  # Faz um Pyro daemon
ns = Pyro4.locateNS()  # Encontra o nome do server
uri2 = daemon.register(Aluno)  # Registrar o como um objeto Pyro
print(uri2)
ns.register(
    "aluno.ufc.kerb", uri2
)  # Registrar o objeto com um nome no servidor de nome
print("Oi. Aluno esta ativo.")
daemon.requestLoop()  # start the event loop of the server to wait for calls
