from Estruturas.Vertice import Vertice
from Estruturas.Regiao import Regiao
from Estruturas.MatrizAdjacencia import MatrizAdjacencia

def main():
    vertices = []
    matriz = MatrizAdjacencia()
    dimension = input().split(" ").pop()
    vehicles_count = input().split(" ").pop()
    sets_count = input().split(" ").pop()
    capacity = input().split(" ").pop()
    input()
    input()
    line = input()

    while (line != "SET_SECTION"):
        arr = line.split(" ")
        v = Vertice(arr[0], int(arr[1]), int(arr[2]))
        vertices.append(v)
        line = input()

    while(line != "DEMAND_SECTION"):
        arr = line.split(" ")
        arr.reverse()
        regiao = Regiao(arr.pop(), "")
        for v in vertices:
            if(v.nome in arr):
                v.regiao = regiao
        line = input()
    
    while(line != "EOF"):
        arr = line.split(" ")
        for v in vertices:
            if(v.regiao.nome == arr[0]):
                v.regiao.demanda = arr[1]
        line = input()

    for v in vertices:
        matriz.adicionaVertice(v)

    matriz.calcularDistancias()
    matriz.imprimirVertices()

main()