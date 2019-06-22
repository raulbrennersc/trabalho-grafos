import sys
import time
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

    def adicionaRegiao(self, r):
        self.regioes.append(r)


    def encontraCaminho2(self, pathArquivoSaida):
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
        
        self.resetaVeiculos()
        
        print("Distancia: " + str(self.distanciaPercorrida))
        f = open(pathArquivoSaida, "a")
        f.write(str(self.distanciaPercorrida))
        f.write("\n")
        for v in self.veiculos:
            for c in v.caminho:
                f.write(c + " ")
            f.write("\n")
        f.close()

    def encontraCaminho(self, pathArquivoSaida):
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
        
        self.resetaVeiculos()
        
        print("Distancia: " + str(self.distanciaPercorrida))
        f = open(pathArquivoSaida, "a")
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
            if(v.regiao != verticeAtual.regiao and (not v.regiao.visitada) and veiculo.capacidade >= v.regiao.demanda):
                if((verticeCandidato == None) or (self.matriz[verticeAtual][v] < self.matriz[verticeAtual][verticeCandidato])):
                    verticeCandidato = v
        return verticeCandidato

    def simulaEscolha(self, veiculo, vertice):
        capacidadeSimulada = veiculo.capacidade - vertice.regiao.demanda
        for r in self.regioesNaoVisitadas:
            possivel = False
            demanda = (0 if(r.nome == vertice.regiao.nome) else r.demanda)
            for v in self.veiculos:
                capacidade = (capacidadeSimulada if(v.nome == veiculo.nome) else v.capacidade)
                if(capacidade >= demanda):
                    possivel = True
                    break
            if(not possivel):
                return False
            
        return True

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



class Veiculo:
    capacidade = 0
    verticeAtual = Vertice
    caminho = []


    def __init__(self, capacidade, vertice):
        self.capacidade = capacidade
        self.verticeAtual = vertice

def main():
    start = time.time()
    print("START")
    pathArquivoEntrada = sys.argv[2] + ".txt"
    pathArquivoSaida = sys.argv[4] + ".txt"
    vertices = []
    regioes = []
    lines = []


    file = open(pathArquivoEntrada, "r")
    rawLines = file.readlines()
    file.close()
    file = open(pathArquivoSaida, "a")
    file.write(sys.argv[2].split("/").pop() + "\n")
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
    matriz.encontraCaminho2(pathArquivoSaida)
    end = time.time()
    timeElapsed = round((end-start), 5)
    print("\nExecutado em: " + str(timeElapsed) + " segundos")

main()