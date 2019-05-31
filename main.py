from Estruturas.Vertice import Vertice
from Estruturas.MatrizAdjacencia import MatrizAdjacencia

def main():
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
        matriz.adicionaVertice(v)
        line = input()
    matriz.calcularDistancias()
    matriz.imprimir()
    



main()