from Estruturas.MatrizAdjacencia import MatrizAdjacencia
from Estruturas.ListaAdjacencia import ListaAdjacencia
from Busca import BuscaProfundidade
from Busca import BuscaLargura
from ExportaArqGraph import ArquivoGraph
def main():
    matriz = MatrizAdjacencia()
    matriz.adicionaVertice("thuza")
    matriz.adicionaVertice("ribo")
    matriz.adicionaVertice("humil")
    matriz.adicionaAresta("thuza", "ribo", "parser")
    matriz.adicionaAresta("thuza", "humil", "parser2")
    matriz.adicionaAresta("ribo", "humil", "topparser")

    print("Matriz adj:\n")
    print(matriz)

    lista = ListaAdjacencia()
    lista.adicionaVertice("thuza")
    lista.adicionaVertice("ribo")
    lista.adicionaVertice("humil")
    lista.adicionaVertice("sil")
    lista.adicionaVertice("job")
    lista.adicionaAresta("thuza", "ribo", "parser")
    lista.adicionaAresta("thuza", "humil", "parser2")
    lista.adicionaAresta("ribo", "humil", "topparser")
    lista.adicionaAresta("sil", "job", "parzer")
    lista.adicionaAresta("thuza", "job", "parzer")

    print("------------------------")
    print("Lista adj:\n")
    print(lista)
    print("------------------------")
    print("Busca em profundidade:\n")
    BuscaProfundidade.buscaProfundidade(lista)
    print("------------------------")
    print("Busca em largura:\n")
    BuscaLargura.buscaLargura(lista)

    arq = ArquivoGraph("teste")
    arq.escreveGrafo(lista)
    arq.close()

main()