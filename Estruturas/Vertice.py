from Estruturas.Regiao import Regiao
class Vertice:
    nome = None
    regiao = Regiao
    x = None
    y = None


    def __init__(self, nome, x, y):
        self.nome = nome
        self.regiao = Regiao("0", 0)
        self.x = x
        self.y = y