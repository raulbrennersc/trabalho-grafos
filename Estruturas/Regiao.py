class Regiao:
    nome = None
    demanda = 0
    vertices = None


    def __init__(self, nome, vertices):
        self.nome = nome
        self.demanda = 0
        self.vertices = vertices