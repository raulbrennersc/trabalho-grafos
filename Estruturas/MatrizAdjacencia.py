from Estruturas.Vertice import Vertice
from Estruturas.Regiao import Regiao
from Estruturas.Veiculo import Veiculo

class MatrizAdjacencia:
    matriz = None
    vertices = [Vertice]
    regioes = [Regiao]
    regioesVisitadas = [Regiao]
    veiculos = [Veiculo]
    capacidadeVeiculo = 0
    quantidadeVeiculos = 0
    distanciaPercorrida = 0


    def __init__(self, capacidadeVeiculo, quantidadeVeiculos, vertices, regioes):
        self.matriz = {}
        self.vertices = vertices
        self.regioes = regioes
        self.regioesVisitadas = self.regioes.copy()
        self.capacidadeVeiculo = capacidadeVeiculo
        self.quantidadeVeiculos = quantidadeVeiculos
        distanciaPercorrida = 0

        for i in range(0, quantidadeVeiculos):
            v = Veiculo(capacidadeVeiculo, self.vertices[0])
            self.veiculos.append(v)

        self.adicionaVertices()

    def adicionaVertices(self):
        for v in self.vertices:
            self.matriz[v] = {}

    def adicionaRegiao(self, r):
        self.regioes.append(r)

    def encontraCaminho(self, pathArquivoSaida):
        while(len(self.regioesVisitadas) > 0):
            melhorVeiculo = Veiculo
            melhorVertice = None
            melhorDistancia = 0
            for veiculo in self.veiculos:
                if(veiculo.capacidade == 0 ):
                    continue
                verticeCandidato =  self.escolherVertice(veiculo)
                if((melhorVertice == None) or (self.matriz[veiculo][verticeCandidato] < melhorDistancia)):
                    melhorVeiculo = veiculo
                    melhorVertice = verticeCandidato
                    melhorDistancia = self.matriz[veiculo.vertice][verticeCandidato]
            
            self.distanciaPercorrida += melhorDistancia
            melhorVeiculo.capacidade -= melhorVertice.regiao.demanda
            melhorVeiculo.caminho.append(melhorVertice.nome)
            melhorVertice.regiao.demanda = 0
            regioesVisitadas.remove(melhorVertice.regiao)

        f = open(pathArquivoSaida, "w")
        f.write(distanciaPercorrida)
        f.write("\n")
        for v in self.veiculos:
            f.write(v.caminho)
            f.write("\n")
        f.close()

        

    def escolherVertice(self, veiculo):
        verticeCandidato = None
        verticeAtual = veiculo.verticeAtual
        for v in self.vertices:
            if(v.regiao != verticeAtual.regiao and v.regiao.demanda > 0 and veiculo.capacidade >= v.regiao.demanda):
                if((verticeCandidato == None) or (self.matriz[verticeAtual][v] < self.matriz[verticeAtual][verticeCandidato])):
                    verticeCandidato = v
        return verticeAtual


    def verificaVeiculos(self, verticeCanditato, veiculoCandidato, distanciaCandidata):
        veiculoFinal = veiculoCandidato
        distanciaFinal = distanciaCandidata
        for veiculo in self.veiculos:
            distanciaParcial = self.matriz[verticeCanditato][veiculo.vertice]
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

