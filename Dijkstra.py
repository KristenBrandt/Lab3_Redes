# ejemplo de uso de Grafo

import networkx as nx
G = nx.DiGraph()

f = open("grafo.txt", "r")
tups = []
for x in f:
    l = x.split()
    l[2] = int(l[2])
    tups.append(tuple(l))

print(tups)

G.add_weighted_edges_from(tups)
# agegar nodos
# G.add_node("Inicio")
# G.add_node("Rosa")
# G.add_node("Tulipan")
# G.add_node("Lirio")
# G.add_node("Girasol")
# G.add_node("Cactus")
# G.add_node("Suculenta")
# G.add_node("Agapanto")

print ("\nNodos: ", G.nodes())

# agregar aristas
# G.add_edge("Inicio", "Rosa",weight=4)
# G.add_edge("Inicio", "Tulipan",weight=3)
# G.add_edge("Inicio", "Lirio",weight=2)
# G.add_edge("Rosa", "Tulipan",weight=10)
# G.add_edge("Rosa", "Girasol",weight=1)
# G.add_edge("Lirio", "Girasol",weight=5)
# G.add_edge("Girasol", "Tulipan",weight=3)
# G.add_edge("Girasol", "Cactus",weight=0)
# G.add_edge("Cactus", "Girasol",weight=2)
# G.add_edge("Cactus", "Agapanto",weight=4)
# G.add_edge("Suculenta", "Agapanto",weight=4)

print ("\nAristas: ", G.edges())

# single source shortest path with Dijkstra

print ("\nRuta mas corta con Dijkstra: ")
print (nx.dijkstra_path(G,'a','e'))
#
#
# print ("Longitud de la ruta mas corta:")
# print (nx.single_source_dijkstra_path_length(G,"Inicio"))
