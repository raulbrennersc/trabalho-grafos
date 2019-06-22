import sys
import time
import igraph

class Regiao:
    nome = None
    demanda = 0
    vertices = None
    visitada = False


    def __init__(self, nome, vertices):
        self.nome = nome
        self.demanda = 0
        self.vertices = vertices

class Vertice:
    nome = None
    regiao = Regiao
    x = None
    y = None


    def __init__(self, nome, x, y):
        self.nome = nome
        self.regiao = Regiao("0", "")
        self.x = x
        self.y = y

class Veiculo:
    capacidade = 0
    verticeAtual = Vertice
    caminho = []


    def __init__(self, capacidade, vertice):
        self.capacidade = capacidade
        self.verticeAtual = vertice

class MatrizAdjacencia:
    matriz = None
    vertices = []
    regioes = []
    regioesNaoVisitadas = []
    veiculos = []
    capacidadeVeiculo = 0
    quantidadeVeiculos = 0
    distanciaPercorrida = 0
    menorDemanda = None


    def __init__(self, capacidadeVeiculo, quantidadeVeiculos, vertices, regioes):
        self.matriz = {}
        self.vertices = vertices
        self.regioes = regioes
        self.regioesNaoVisitadas = self.regioes.copy()
        self.capacidadeVeiculo = capacidadeVeiculo
        self.quantidadeVeiculos = quantidadeVeiculos
        distanciaPercorrida = 0

        for i in range(0, quantidadeVeiculos):
            v = Veiculo(capacidadeVeiculo, self.vertices[0])
            v.nome = str(i)
            v.caminho = [vertices[0].nome]
            self.veiculos.append(v)

        self.vertices[0].regiao.visitada = True

        self.calcularMenorDemanda()

        self.adicionaVertices()

    def adicionaVertices(self):
        for v in self.vertices:
            self.matriz[v] = {}

    def calcularMenorDemanda(self):
        for r in self.regioesNaoVisitadas:
            if(self.menorDemanda == None or self.menorDemanda.demanda == 0 or r.demanda < self.menorDemanda.demanda):
                self.menorDemanda = r

    def encontraCaminho(self, pathArquivoSaida, pathArqSol, pathImgCaminho):
        inicio = time.time()
        for veiculo in self.veiculos:
            while(veiculo.capacidade >= self.menorDemanda.demanda and len(self.regioesNaoVisitadas) > 0):
                melhorVertice =  self.escolherVertice(veiculo)
                if(melhorVertice == None):
                    break
                melhorDistancia = self.matriz[veiculo.verticeAtual][melhorVertice]
                self.distanciaPercorrida += melhorDistancia
                veiculo.capacidade -= melhorVertice.regiao.demanda
                veiculo.caminho.append(melhorVertice.nome)
                melhorVertice.regiao.demanda = 0
                melhorVertice.regiao.visitada = True
                veiculo.verticeAtual = melhorVertice
                self.regioesNaoVisitadas.remove(melhorVertice.regiao)
                self.calcularMenorDemanda()
        
        self.retornaVeiculos()
        
        timeElapsed = str(round((time.time() - inicio), 5))

        f = open(pathArqSol, "w")
        for v in self.veiculos:
            for c in v.caminho:
                f.write(c + " ")
            f.write("\n")
        f.close()
        
        if(pathImgCaminho is not ""):
            g = igraph.Graph(directed=True)
            labels = []
            for v in self.veiculos:
                v.caminho[0] = "veiculo " + str(int(v.nome) + 1)
                aux = ""
                for c in v.caminho:
                    labels.append(c)
                    g.add_vertex(c)
                    if(aux is not ""):
                        g.add_edge(aux, c)
                    aux = c
                g.add_edge(aux, v.caminho[0])
            igraph.plot(g, vertex_label=labels, target=pathImgCaminho)

        f = open(pathArquivoSaida, "a")
        f.write(str(round(self.distanciaPercorrida, 2)) + " " + timeElapsed + "\n")
        f.close()

    def retornaVeiculos(self):
        for v in self.veiculos:
            if(v.verticeAtual != self.vertices[0]):
                self.retornaVeiculo(v)

    def retornaVeiculo(self, veiculo):
        veiculo.capacidade = self.capacidadeVeiculo
        self.distanciaPercorrida += self.matriz[veiculo.verticeAtual][self.vertices[0]]

    def escolherVertice(self, veiculo):
        verticeCandidato = None
        verticeAtual = veiculo.verticeAtual
        for v in self.vertices:
            if(v.regiao != verticeAtual.regiao and (not v.regiao.visitada) and veiculo.capacidade >= v.regiao.demanda):
                if((verticeCandidato == None) or (self.matriz[verticeAtual][v] < self.matriz[verticeAtual][verticeCandidato])):
                    verticeCandidato = v
        return verticeCandidato

    def calcularDistancia(self, v1, v2):
        return ((((v1.x - v2.x) ** 2) + ((v1.y - v2.y) ** 2) )** 0.5)
        
#Calcula a distancia entre dois pontos no plano
    def calcularDistancias(self):
        for v1 in self.vertices:
            for v2 in self.vertices:
                d = (0 if(v1.regiao == v2.regiao) else self.calcularDistancia(v1, v2))
                self.matriz[v1][v2] = d
                self.matriz[v2][v1] = d

def main():
    pathArquivoEntrada = ""
    pathArquivoSaida = ""
    pathArqSol = ""
    pathImgCaminho = ""

    for i in range(0, len(sys.argv)):
        if(sys.argv[i] == "-in"):
            pathArquivoEntrada = sys.argv[i+1] + ".txt"
        elif(sys.argv[i] == "-out"):
            pathArquivoSaida = sys.argv[i+1] + ".txt"
        elif(sys.argv[i] == "-img"):
            pathImgCaminho = sys.argv[i+1]
            pathArqSol = sys.argv[i+2] + ".txt"
        
    vertices = []
    regioes = []
    lines = []


    file = open(pathArquivoEntrada, "r")
    rawLines = file.readlines()
    file.close()
    file = open(pathArquivoSaida, "a")
    file.write(sys.argv[2].split("/").pop() + " ")
    file.close()
    for line in rawLines:
        lines.append(line.replace("\n", ""))
    lines.reverse()
    
    line = lines.pop()
    dimension = int(line.split(" ").pop())
    line = lines.pop()
    vehicles_count = int(line.split(" ").pop())
    line = lines.pop()
    sets_count = int(line.split(" ").pop())
    line = lines.pop()
    capacity = int(line.split(" ").pop())


    lines.pop()
    lines.pop()

    line = lines.pop()
    while (line != "SET_SECTION"):
        arr = line.split(" ")
        v = Vertice(arr[0], int(arr[1]), int(arr[2]))
        vertices.append(v)
        line = lines.pop()

    line = lines.pop()
    while(line != "DEMAND_SECTION"):
        arr = line.split(" ")
        arr.pop()
        arr.reverse()
        nomeRegiao = arr.pop()
        regiao = Regiao(nomeRegiao, arr)
        regioes.append(regiao)
        line = lines.pop()
    
    for regiao in regioes:
        for v in vertices:
            if(v.nome in regiao.vertices):
                v.regiao = regiao

    while(line != "EOF"):
        arr = line.split(" ")
        for regiao in regioes:
            if(regiao.nome == arr[0]):
                regiao.demanda = int(arr[1])
        line = lines.pop()

    matriz = MatrizAdjacencia(capacity, vehicles_count, vertices, regioes)

    matriz.calcularDistancias()
    matriz.encontraCaminho(pathArquivoSaida, pathArqSol, pathImgCaminho)

main()