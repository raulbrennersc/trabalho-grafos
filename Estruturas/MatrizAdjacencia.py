import time
import igraph
from Estruturas.Vertice import Vertice
from Estruturas.Regiao import Regiao
from Estruturas.Veiculo import Veiculo

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
        print("\nExecutado em: " + str(timeElapsed) + " segundos")
        print("Distância: " + str(round(self.distanciaPercorrida, 2)))

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

    def encontraCaminhoAntigo(self, pathArquivoSaida):
        while(len(self.regioesNaoVisitadas) > 0):
            melhorVeiculo = Veiculo
            melhorVertice = None
            melhorDistancia = 0
            for veiculo in self.veiculos:
                parPerfeito = self.parPerfeito(veiculo)
                if(parPerfeito != None):
                    melhorVeiculo = veiculo
                    melhorVertice = parPerfeito
                    melhorDistancia = self.matriz[melhorVeiculo.verticeAtual][melhorVertice]
                    break

                verticeCandidato =  self.escolherVertice(veiculo)
                if(verticeCandidato == None):
                    continue
                if((melhorVertice == None) or (self.matriz[veiculo.verticeAtual][verticeCandidato] < melhorDistancia)):
                    melhorVeiculo = veiculo
                    melhorVertice = verticeCandidato
                    melhorDistancia = self.matriz[melhorVeiculo.verticeAtual][melhorVertice]
            self.distanciaPercorrida += melhorDistancia
            melhorVeiculo.capacidade -= melhorVertice.regiao.demanda
            melhorVeiculo.caminho.append(melhorVertice.nome)
            melhorVertice.regiao.demanda = 0
            melhorVertice.regiao.visitada = True
            melhorVeiculo.verticeAtual = melhorVertice
            self.regioesNaoVisitadas.remove(melhorVertice.regiao)
            self.calcularMenorDemanda()
        
        self.retornaVeiculos()
        
        print("Distancia: " + str(self.distanciaPercorrida))
        f = open(pathArquivoSaida, "a")
        f.write(str(self.distanciaPercorrida))
        f.write("\n")
        for v in self.veiculos:
            for c in v.caminho:
                f.write(c + " ")
            f.write("\n")
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

    def parPerfeito(self, veiculo):
        melhorVertice = None
        for r in self.regioesNaoVisitadas:
            if(r.demanda == veiculo.capacidade):
                for v in self.vertices:
                    if(v.regiao.nome != r.nome):
                        continue
                    if(melhorVertice == None or (self.matriz[veiculo.verticeAtual][v] <  self.matriz[veiculo.verticeAtual][melhorVertice])):
                        melhorVertice = v
            if(melhorVertice != None):
                break;
        return melhorVertice

    def calcularDistancia(self, v1, v2):
        return ((((v1.x - v2.x) ** 2) + ((v1.y - v2.y) ** 2) )** 0.5)
        
#Calcula a distancia entre dois pontos no plano
    def calcularDistancias(self):
        for v1 in self.vertices:
            for v2 in self.vertices:
                d = (0 if(v1.regiao == v2.regiao) else self.calcularDistancia(v1, v2))
                self.matriz[v1][v2] = d
                self.matriz[v2][v1] = d

