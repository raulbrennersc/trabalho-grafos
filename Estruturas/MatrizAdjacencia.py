from Estruturas.Vertice import Vertice

class MatrizAdjacencia:
    matriz = None
    vertices = None

    def __init__(self):
        self.matriz = {}
        self.vertices = []

    def adicionaVertice(self, v):
        self.vertices.append(v)

        self.matriz[v.nome] = {}
        for chave in self.matriz:
            self.matriz[v.nome][chave] = ""
            self.matriz[chave][v.nome] = ""

    def adicionaAresta(self, nomeV1, nomeV2, relacao):
        if(self.matriz[nomeV1][nomeV2] != ""):
            return "Ja ha uma relacao entre os vertices"
        self.matriz[nomeV1][nomeV2] = relacao
        self.matriz[nomeV2][nomeV1] = relacao

    def imprimir(self):
        for v1 in self.vertices:
            for v2 in self.vertices:
                print(self.matriz[v1.nome][v2.nome])

#Calcula a distancia entre dois pontos no plano
    def calcularDistancias(self):
        for v1 in self.vertices:
            for v2 in self.vertices:
                d = ((((v1.x - v2.x) ** 2) + ((v1.y - v2.y) ** 2) )** 0.5)
                self.matriz[v1.nome][v2.nome] = d
                self.matriz[v2.nome][v1.nome] = d

#Imprime as informacoes sobre todos os vertices contidos na matriz
    def imprimirVertices(self):
        for v in self.vertices:
            print(v.nome + ": Regiao: " + v.regiao.nome)


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

    def saoVizinhos(self, v1, v2):
        if(v1 not in self.matriz):
            return False
        if(v2 not in self.matriz):
            return False
        if(self.matriz[v1][v2] == ""):
            return False
        return True

    def getVizinhos(self, v):
        vizinhos = []
        for chave in self.matriz:
            if(self.matriz[v][chave] != ""):
                vizinhos.append(chave)
        return vizinhos

    def retornaRelacao(self, v1, v2):
        return self.matriz[v1][v2]
