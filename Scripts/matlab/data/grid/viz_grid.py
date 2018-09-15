import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pygraphviz
import random
from networkx.drawing.nx_agraph import graphviz_layout

def draw_graph(graph, install_nodes, soc_katz, katz):
    install_graph = nx.Graph()
    for node in install_nodes:
        install_graph.add_node(node)
        

    m_katz = []
    s_katz = []
    for node in sorted(graph.nodes()):
        m_katz.append(soc_katz[node])
        s_katz.append(katz[node])

    pos = graphviz_layout(graph, prog='sfdp')
    pos2 = {}
    for node in install_nodes:
        pos2[node] = pos[node]
    katz2 = [soc_katz[node] for node in install_graph.nodes()]

    #plt.subplot(1, 2, 1)
    nodes = nx.draw_networkx_nodes(graph,pos,node_color=m_katz, node_size =100,
                cmap=plt.cm.Blues, linewidths=0.1)
    #nodes2 = nx.draw_networkx_nodes(install_graph, pos2,node_color=katz2, node_size =100,
 #               cmap=plt.cm.Blues, vmin=min(m_katz), vmax=max(m_katz),  linewidths=1)

   # nodes2.set_edgecolor('r')
    edges = nx.draw_networkx_edges(graph,pos,edge_color='gray',width=0.5)
    plt.colorbar(nodes)
    plt.axis('off') 




    #plt.subplot(1, 2, 2)
    #plt.plot(katz, soc_katz, 'o')
    #plt.xlabel("Katz")
    #plt.ylabel("SOC-Katz")
    #plt.savefig("soc_katz_6.eps") 
    plt.show()


if __name__ == '__main__':
    
    graphfile = '/home/hushiji/Research/centrality/Scripts/data/grid/grid10x10.txt'
    graph = nx.read_edgelist(graphfile, nodetype=int)
    data = np.genfromtxt('/home/hushiji/Research/centrality/Scripts/data/grid/\
exp_cen.txt').T
    katz, soc_katz, install_marker = data
    mapping=dict(zip(sorted(graph.nodes()),range(nx.number_of_nodes(graph))))
    graph = nx.relabel_nodes(graph,mapping) 
    install_nodes = [i-1 for i, _ in enumerate(install_marker, start=1) if int(_) ==1]

    draw_graph(graph, install_nodes, soc_katz, katz)
    #plt.plot(katz, soc_katz, 'o')
    #plt.xlabel("Katz")
    #plt.ylabel("SOC-Katz")
    #plt.savefig("soc_katz_scatter_8.eps") 
    
