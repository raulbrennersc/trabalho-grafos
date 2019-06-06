from Estruturas.Vertice import Vertice
class Veiculo:
    capacidade = 0
    verticeAtual = Vertice
    caminho = []


    def __init__(self, capacidade, vertice):
        self.capacidade = capacidade
        self.verticeAtual = vertice