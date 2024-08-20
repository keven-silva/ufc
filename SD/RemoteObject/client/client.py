import Pyro4

# Usando os metodos da interface do objeto distribuido
aluno = Pyro4.Proxy("PYRONAME:aluno.ufc.kerb" + "@localhost:9090")
print(aluno.getDisciplina())
