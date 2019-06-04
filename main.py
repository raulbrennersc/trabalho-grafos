import sys
import time
from Estruturas.Vertice import Vertice
from Estruturas.Regiao import Regiao
from Estruturas.MatrizAdjacencia import MatrizAdjacencia

def main():
    start = time.time()
    print("START")
    pathArquivoEntrada = sys.argv[2] + ".txt"
    pathArquivoSaida = sys.argv[4] + ".txt"
    vertices = []
    lines = []


    file = open(pathArquivoEntrada, "r")
    rawLines = file.readlines()
    file.close()
    for line in rawLines:
        lines.append(line.replace("\n", ""))
    lines.reverse()
    
    line = lines.pop()
    dimension = line.split(" ").pop()
    line = lines.pop()
    vehicles_count = line.split(" ").pop()
    line = lines.pop()
    sets_count = line.split(" ").pop()
    line = lines.pop()
    capacity = line.split(" ").pop()

    matriz = MatrizAdjacencia(capacity, vehicles_count)

    lines.pop()
    lines.pop()

    line = lines.pop()
    while (line != "SET_SECTION"):

        arr = line.split(" ")
        v = Vertice(arr[0], int(arr[1]), int(arr[2]))
        vertices.append(v)
        line = lines.pop()

    while(line != "DEMAND_SECTION"):
        arr = line.split(" ")
        arr.reverse()
        regiao = Regiao(arr.pop(), "")
        for v in vertices:
            if(v.nome in arr):
                v.regiao = regiao
        line = lines.pop()
    
    while(line != "EOF"):
        arr = line.split(" ")
        for v in vertices:
            if(v.regiao.nome == arr[0]):
                v.regiao.demanda = arr[1]
        line = lines.pop()

    for v in vertices:
        matriz.adicionaVertice(v)

    matriz.calcularDistancias()
    ##matriz.imprimirVertices(pathArquivoSaida)
    end = time.time()
    timeElapsed = (end-start)*1000
    print("Executado em: " + str(timeElapsed) + " ms")

main()