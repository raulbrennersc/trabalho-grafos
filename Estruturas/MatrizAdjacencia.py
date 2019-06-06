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
            v.caminho = [vertices[0].nome]
            self.veiculos.append(v)

        for r in self.regioes:
            if(r.demanda <= 0):
                self.regioesNaoVisitadas.remove(r)

        self.calcularMenorDemanda()

        self.adicionaVertices()

    def adicionaVertices(self):
        for v in self.vertices:
            self.matriz[v] = {}

    def calcularMenorDemanda(self):
        for r in self.regioesNaoVisitadas:
            if(self.menorDemanda == None or self.menorDemanda.demanda == 0 or r.demanda < self.menorDemanda.demanda):
                self.menorDemanda = r

    def adicionaRegiao(self, r):
        self.regioes.append(r)

    def encontraCaminho(self, pathArquivoSaida):
        while(len(self.regioesNaoVisitadas) > 0):
            melhorVeiculo = Veiculo
            melhorVertice = None
            melhorDistancia = 0
            for veiculo in self.veiculos:
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
            melhorVeiculo.verticeAtual = melhorVertice
            self.regioesNaoVisitadas.remove(melhorVertice.regiao)
            self.calcularMenorDemanda()
        
        self.resetaVeiculos()
        
        print("Distancia: " + str(self.distanciaPercorrida))
        f = open(pathArquivoSaida, "w")
        f.write(str(self.distanciaPercorrida))
        f.write("\n")
        for v in self.veiculos:
            for c in v.caminho:
                f.write(c + " ")
            f.write("\n")
        f.close()

    def resetaVeiculos(self):
        for v in self.veiculos:
            if(v.verticeAtual != self.vertices[0]):
                self.resetaVeiculo(v)

    def resetaVeiculo(self, veiculo):
        veiculo.capacidade = self.capacidadeVeiculo
        self.distanciaPercorrida += self.matriz[veiculo.verticeAtual][self.vertices[0]]
        veiculo.caminho.append(self.vertices[0].nome)

    def escolherVertice(self, veiculo):
        verticeCandidato = None
        verticeAtual = veiculo.verticeAtual
        for v in self.vertices:
            if(v.regiao != verticeAtual.regiao and v.regiao.demanda > 0 and veiculo.capacidade >= v.regiao.demanda):
                if((verticeCandidato == None) or (self.matriz[verticeAtual][v] < self.matriz[verticeAtual][verticeCandidato])):
                    verticeCandidato = v
        return verticeCandidato


    def verificaVeiculos(self, verticeCanditato, veiculoCandidato, distanciaCandidata):
        veiculoFinal = veiculoCandidato
        distanciaFinal = distanciaCandidata
        for veiculo in self.veiculos:
            distanciaParcial = self.matriz[verticeCanditato][veiculo.verticeAtual]
            if(veiculo.capacidade > verticeCanditato.demanda and distanciaParcial < distanciaFinal):
                veiculoFinal = veiculo
                distanciaFinal = distanciaParcial

        self.distanciaPercorrida += distanciaFinal


    def calcularDistancia(self, v1, v2):
        return ((((v1.x - v2.x) ** 2) + ((v1.y - v2.y) ** 2) )** 0.5)
        
#Calcula a distancia entre dois pontos no plano
    def calcularDistancias(self):
        for v1 in self.vertices:
            for v2 in self.vertices:
                d = (0 if(v1.regiao == v2.regiao) else self.calcularDistancia(v1, v2))
                self.matriz[v1][v2] = d
                self.matriz[v2][v1] = d

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

