from __future__ import division

#import pygraphviz
import sys
import argparse
import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy import sparse
import scipy
#from networkx.drawing.nx_agraph import graphviz_layout
from networkx.readwrite import json_graph
import os, sys


def create_layer_graph(graph, levels, placement):
    layer_graph = nx.DiGraph()
    
    for u, v in graph.edges():
        for i in range(levels, 1, -1):
            node_i = (u,i)
            if u in placement:           
                node_j = (v, levels)
                layer_graph.add_edge(node_i, node_j)
            else:
                node_j = (v, i-1)
                layer_graph.add_edge(node_i, node_j)
                
            node_i = (v,i)
            if v in placement:           
                node_j = (u, levels)
                layer_graph.add_edge(node_i, node_j)
            else:
                node_j = (u, i-1)
                layer_graph.add_edge(node_i, node_j)
        if u not in placement:
            layer_graph.add_edge((u,1), 'absorb')
        if v not in placement:
            layer_graph.add_edge((v,1), 'absorb')
            

    return layer_graph
        
if __name__ == '__main__':
    
    graph = nx.karate_club_graph()
    graph = nx.erdos_renyi_graph(50,0.3)
    #graph = nx.grid_2d_graph(2,2)
    #graph = nx.Graph()
    #graph.add_edge(1,2)
    #graph.add_edge(2,3)
    #graph.add_edge(3,1)
    
    levels = 3
    placement = [1, 2, 3,4,5]
    #placement = []
    
    layer_graph = create_layer_graph(graph, levels, placement)
    
    nodes = sorted([i for i in layer_graph.nodes() if i!= 'absorb'],key=lambda x: x[1], reverse=True)
    nodes.append('absorb')
    #print(nodes)

    print('number_of_nodes:', nx.number_of_nodes(graph), 'layered:', nx.number_of_nodes(layer_graph))
    mapping = dict(zip(nodes, range(len(nodes))))
    print(mapping)
    H = nx.relabel_nodes(layer_graph, mapping)
    Adj = nx.adjacency_matrix(H,  nodelist=range(len(nodes)))
    plt.spy(Adj**100)
    plt.show()
    
                
    
