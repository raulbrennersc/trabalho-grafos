import sys
import time
from Estruturas.Vertice import Vertice
from Estruturas.Regiao import Regiao
from Estruturas.MatrizAdjacencia import MatrizAdjacencia

def main():
    start = time.time()
    print("START")
    pathArquivoEntrada = ""
    pathArquivoSaida = ""
    pathImgSol = ""
    pathImgCaminho = ""

    for i in range(0, len(sys.argv)):
        if(sys.argv[i] == "-in"):
            pathArquivoEntrada = sys.argv[i+1] + ".txt"
        elif(sys.argv[i] == "-out"):
            pathArquivoSaida = sys.argv[i+1] + ".txt"
        elif(sys.argv[i] == "-img"):
            pathImgCaminho = sys.argv[i+1] + ".png"
            pathImgSol = sys.argv[i+2] + ".png"
        
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
    matriz.encontraCaminho2(pathArquivoSaida, pathImgSol, pathImgCaminho)
    end = time.time()
    timeElapsed = round((end-start), 5)
    print("\nExecutado em: " + str(timeElapsed) + " segundos")

main()