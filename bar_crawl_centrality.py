from __future__ import division

import pygraphviz
import sys
import argparse
import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy import sparse
import scipy, scipy.io
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.readwrite import json_graph
import os, sys


def read_graph(graphfile,labelfile):
  
  edges = np.genfromtxt(graphfile, dtype='int')
  labels = np.genfromtxt(labelfile, dtype='int')
  
  graph = nx.DiGraph()
  
  for u,v in edges:
    
    if u != v:
      graph.add_edge(u,v)
  
  for u, l in labels:
    if u in graph.nodes():
      graph.node[u]["community"] = l
  


  #print(nx.number_of_nodes(graph))
  #graph = nx.convert_node_labels_to_integers(graph)
  #pos = graphviz_layout(graph, prog='sfdp')
  
  #nx.draw(graph, pos,  node_size=10, arrows=False,with_labels=False)
  #plt.show()
  
  return graph


def rank_nodes(graph, steps, labelled_nodes):
  
  n = nx.number_of_nodes(graph)
  Adj = nx.adjacency_matrix(graph)
  I = sparse.identity(n, dtype='int')
  J = np.array([1 if i in labelled_nodes else 0 for i in range(n)])
  J = np.diag(J)

  one_vec = np.ones(n)
  D = Adj.dot(one_vec)
  
  B = []
  block_row = [None for i in range(steps)]
  block_row[0] = Adj*J
  block_row[ 1] = Adj*(I-J)
  B.append(block_row)
  for row in range(1,steps-1):
    block_row = [None for i in range(steps)]
    block_row[0] = (I-J)*Adj*J
    block_row[row + 1] = (I-J)*Adj*(I-J)
    B.append(block_row)
  block_row = [None for i in range(steps)]
  block_row[0] = Adj*J
  B.append(block_row)
  B = sparse.bmat(B)
  
  I_nXsteps = sparse.identity(n*steps, dtype='int')
  
  X = sparse.bmat([[I] for _ in range(steps)])
  zero_nxn = I-I
  Y = [[zero_nxn] for _ in range(steps)]
  Y[0] = [I]
  Y = sparse.bmat(Y)

  #change type
  Adj = Adj.astype(float)
  B = B.astype(float)
  Y = Y.astype(float)
  X = X.astype(float)
  
  eig_max_A =  sparse.linalg.eigs(Adj, k=1, return_eigenvectors=False)
  eig_max_B = sparse.linalg.eigs(B, k=1, return_eigenvectors=False)
  alpha1 = list(eig_max_A)[0].real
  alpha2 = list(eig_max_B)[0].real
  
  


if __name__ == '__main__':
  graphfile = "/home/hushiji/Research/centrality/Data/email-Eu-core.txt"
  labelfile = "/home/hushiji/Research/centrality/Data/email-Eu-core-department-labels.txt"
  
  #graph = read_graph(graphfile, labelfile)
  graph = nx.karate_club_graph()
  steps = 4
  labelled_nodes = graph.nodes()[:10]
  rank_nodes(graph, steps, labelled_nodes)
