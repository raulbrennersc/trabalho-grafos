from Estruturas.Vertice import Vertice

class MatrizAdjacencia:
    matriz = None
    vertices = None
    capacidadeVeiculo = None
    quantidadeVeiculos = None


    def __init__(self, capacidadeVeiculo, quantidadeVeiculos):
        self.matriz = {}
        self.vertices = []
        self.capacidadeVeiculo = capacidadeVeiculo
        self.quantidadeVeiculos = quantidadeVeiculos

    def adicionaVertice(self, v):
        self.vertices.append(v)

        self.matriz[v.nome] = {}
        for chave in self.matriz:
            self.matriz[v.nome][chave] = ""
            self.matriz[chave][v.nome] = ""

    def encontraCaminho(self):
        regioesVisitadas = []
        return

    def retornaDistancia(self, v1, v2):
        return ((((v1.x - v2.x) ** 2) + ((v1.y - v2.y) ** 2) )** 0.5)
        
#Calcula a distancia entre dois pontos no plano
    def calcularDistancias(self):
        for v1 in self.vertices:
            for v2 in self.vertices:
                d = self.retornaDistancia(v1, v2)
                self.matriz[v1.nome][v2.nome] = d
                self.matriz[v2.nome][v1.nome] = d

#Imprime as informacoes sobre todos os vertices contidos na matriz
    def imprimirVertices(self, pathArquivoSaida):
        f = open(pathArquivoSaida, "w")
        for v in self.vertices:
            f.write(v.nome + ": Regiao: " + v.regiao.nome + "\n")
        f.close()


    def __str__(self):
        saida = "\t"
        for linha in self.matriz:
            saida += str(linha) + "\t"
        saida += "\n"
        for coluna in self.matriz:
            saida += str(coluna)
            for linha in self.matriz:
                saida += ("\t" + str(self.matriz[linha][coluna]))
            saida += "\n"
        return saida

    def saoConterraneos(self, v1, v2):
        return v1.regiao.nome == v2.regiao.nome

