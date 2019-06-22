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

class TrabalhoGrafos:
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

        #Inicializa os inicializa os veículos colocando cada um no vértice inicial (depoósito)
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

    #Função que calcula qual é a região ainda não visitada com a menor demanda
    def calcularMenorDemanda(self):
        for r in self.regioesNaoVisitadas:
            if(self.menorDemanda == None or self.menorDemanda.demanda == 0 or r.demanda < self.menorDemanda.demanda):
                self.menorDemanda = r

    #Função que tenta encontrar um caminho viável para a solução do problema
    def encontraCaminho(self, pathArquivoSaida, pathArqSol, pathImgCaminho):
        #Inicia a contagem de tempo
        inicio = time.time()
        for veiculo in self.veiculos:
            #Para cada veículo disponível o algorítmo tenta visitar o máximo de regiões possíveis
            #Nem sempre todos os veículos serão utilizados
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
                #Atualiza a menor demanda entre as regiões não visitadas
                self.calcularMenorDemanda()
        
        #Retorna todos os veículos para o vértice inicial (depósito), exceto aqueles que já estão lá
        #Não adiciona o vértice incial ao caminho pois foi solicitado no trabalho que no arquivo de solução
        #o último vértice não fosse inserido
        self.retornaVeiculos()
        
        #calcula o tempo gasto para calcular o caminho encontrado
        timeElapsed = str(round((time.time() - inicio), 5))

        #Escreve no arquivo de solucão o caminho percorrido por cada veículo
        f = open(pathArqSol, "w")
        for v in self.veiculos:
            for c in v.caminho:
                f.write(c + " ")
            f.write("\n")
        f.close()
        
        #Gera uma imagem demonstrando o caminho percorrido por cada veículo e depois retornando para o depósito
        #Imagem gerada utilizando a biblioteca iGraph
        if(pathImgCaminho is not ""):
            g = igraph.Graph(directed=True)
            labels = []
            for v in self.veiculos:
                #No vetor que representa o caminho percorrido por cada veículo,
                #substitui o nome do vértice inicial por "veículo (número do veículo)"
                #para adicionar clareza à imagem
                v.caminho[0] = "veiculo " + str(int(v.nome) + 1)
                aux = ""
                for c in v.caminho:
                    labels.append(c)
                    g.add_vertex(c)
                    if(aux is not ""):
                        g.add_edge(aux, c)
                    aux = c
                #Insere o vértice inicial no fim do vetor que representa o caminho percorrido pelo veículo
                #pois ao contrário do arquivo de solução, na imagem com os caminihos deve apresentar o retorno de cada veículo ao vértice inicial.
                #Na imagem gerada, caso algum vértice aparece sem nenhuma ligação (desconexo), significa que o veículo correspondente àquele caminho
                #não foi utilizado para atender às demandas das regiões daquele problema
                g.add_edge(aux, v.caminho[0])
            igraph.plot(g, vertex_label=labels, target=pathImgCaminho)

        #Adiciona ao arquivo de resultados o resultado do problema para o qual o programa foi executado sem apagar os últimos registros no arquivo
        f = open(pathArquivoSaida, "a")
        f.write(str(round(self.distanciaPercorrida, 2)) + " " + timeElapsed + "\n")
        f.close()

    #Retorna todos os veículos para o vértice inicial (depósito), exceto aqueles que já estão lá
    def retornaVeiculos(self):
        for v in self.veiculos:
            if(v.verticeAtual != self.vertices[0]):
                self.distanciaPercorrida += self.matriz[v.verticeAtual][self.vertices[0]]
    
    #Função que retorna o melhor vértice para um dado veículo, ou seja,
    #retorna o vértice mais próximo que pertence à uma região não visitada
    def escolherVertice(self, veiculo):
        verticeCandidato = None
        verticeAtual = veiculo.verticeAtual
        for v in self.vertices:
            if(v.regiao != verticeAtual.regiao and (not v.regiao.visitada) and veiculo.capacidade >= v.regiao.demanda):
                if((verticeCandidato == None) or (self.matriz[verticeAtual][v] < self.matriz[verticeAtual][verticeCandidato])):
                    verticeCandidato = v
        return verticeCandidato

    #Funcão que calcula a distância euclidiana entre dosi vértices
    def calcularDistancia(self, v1, v2):
        return ((((v1.x - v2.x) ** 2) + ((v1.y - v2.y) ** 2) )** 0.5)
        
    #Funcão que utiliza a função anterior para calcular a distancia entre todos os vértices de regiões diferentes do grafo
    #quando dois vértices estão na mesma região a distância entre eles é setada para 0.
    #Nesse caso não existe necessidade de calcular a distância entre dois vértices da mesma região pois
    #nunca existirá um movimento que inicia em um vértice e termina em um outro vértce da mesma região
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

    #Lê os parametros passados na linha de comando
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

    #Leitura do arquivo de entrada para preencher as listas de vertices e regiões
    #a lista de veículos será montada quando o grafo for montado, no primeiro momento somente
    #a quantidade de veículos e a capacidade é armazenada
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

    #Inicializa a estrutura responsável por encontrar um caminho viável para o problema
    matriz = TrabalhoGrafos(capacity, vehicles_count, vertices, regioes)

    matriz.calcularDistancias()
    matriz.encontraCaminho(pathArquivoSaida, pathArqSol, pathImgCaminho)

main()