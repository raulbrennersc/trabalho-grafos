from Estruturas.Vertice import Vertice
class Veiculo:
    capacidade = 0
    verticeAtual = Vertice
    caminho = None


    def __init__(self, capacidade, vertice):
        self.capacidade = capacidade
        self.vertice = vertice
        self.caminho = ["1"]