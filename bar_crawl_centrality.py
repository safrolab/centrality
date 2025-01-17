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
from scipy import stats
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
  


  print(nx.number_of_nodes(graph))
  graph = nx.convert_node_labels_to_integers(graph)
  #pos = graphviz_layout(graph, prog='sfdp')
  
  #nx.draw(graph, pos,  node_size=10, arrows=False,with_labels=True)
  #plt.show()
  
  return graph

def normalized(a):

  return (a - a.min())/(a.max() - a.min())

def get_node_rank(centrality):
  
  return [i for _, i in sorted(zip(centrality, range(len(centrality))))]
  
def get_correlation(X, Y, labelled_nodes, steps):


    coef = np.corrcoef(X,Y)
    slope, intercept, r_value, p_value, std_err = stats.linregress(X,Y)
    r_squared = r_value**2
    #print('node:', labelled_nodes, coef[0][1], r_value, r_value**2)
    m,b=np.polyfit(X,Y,1)
    x = np.linspace(0,max(X))
    y = m*x + b
    plt.plot(X,Y, 'o')
    plt.plot(x,y,'k')
    plot_info = r'$\omega='+str(len(labelled_nodes))+ ',m='+str(steps)+',R^2='+str("%.3f" %r_squared)+'$'
    plt.annotate(plot_info, xy=(1, 0), xycoords='axes fraction', fontsize=16,
                xytext=(-5, 5), textcoords='offset points',
                ha='right', va='bottom')
    plt.xlabel("Katz")
    plt.ylabel("Bounded Katz")
    plt.ylim(0)
    plt.show()
 
def rank_nodes(graph, steps, labelled_nodes):
  
  n = nx.number_of_nodes(graph)
  Adj = nx.adjacency_matrix(graph, nodelist=sorted(graph.nodes()))
  
  I = sparse.identity(n, dtype='int')
  I = scipy.sparse.csc_matrix(I)
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
  
  X = sparse.bmat([[I] for _ in range(steps)])
  zero_nxn = I-I
  Y = [[zero_nxn] for _ in range(steps)]
  Y[0] = [I]
  Y = sparse.bmat(Y)

  #change type
  Adj = Adj.astype(float)
  Adj = scipy.sparse.csc_matrix(Adj)
  B = B.astype(float)
  B = scipy.sparse.csc_matrix(B)
  Y = Y.astype(float)
  Y = scipy.sparse.csc_matrix(Y)
  X = X.astype(float)
  X = scipy.sparse.csc_matrix(X)

  
  compare = True
  if compare:
    
    eig_max_A =  sparse.linalg.eigs(Adj, k=1, return_eigenvectors=False, which='LM',maxiter=34*10000)

    eig_max_B = sparse.linalg.eigs(B, k=1, return_eigenvectors=False, which='LM', maxiter=34*10000)
    eig_max_A = abs(list(eig_max_A)[0].real)
    #eig_max_B = list(eig_max_B)[0].real 
    alpha1 = 1/eig_max_A - 0.03
    #alpha2 = 1/eig_max_B - 0.02
    alpha2 = 1/eig_max_A  - 0.01
    
    #print(eig_max_A, eig_max_B)
    W1 = sparse.linalg.inv(I - alpha1*Adj)
    
    I_nXsteps = sparse.identity(n*steps, dtype='int')
    I_nXsteps = scipy.sparse.csc_matrix(I_nXsteps)
    W2 = sparse.linalg.inv(I_nXsteps  - alpha2*B)
    #W1 = W1*(alpha1*Adj)**(steps )
    #W2 = W2*(alpha2*B)**(steps )
    W2 = Y.T * W2*X
    C1 = W1.dot(np.ones(n))
    initial_centrality = [1 if node not in labelled_nodes else 2 for node in sorted(graph.nodes())]
    initial_centrality = np.array(initial_centrality)
    C3 = W1.dot(initial_centrality)
    #Deg_centralilty = [nx.degree(graph, node) for node in sorted(graph.nodes())]
    C2 = W2.dot(np.ones(n))
    rank_katz, mod_rank_katz, bounded_katz = get_node_rank(C1),get_node_rank(C3),get_node_rank(C2)
    for i, cen in enumerate(C2):
      if cen <0:
        raise ValueError("matrix inverse did not give correct result")
    for i in range(len(rank_katz)):
      print rank_katz[i], mod_rank_katz[i], bounded_katz[i]
    #C1 = normalized(C1)
    #C2 = normalized(C2)
    
    get_correlation(C3, C2, labelled_nodes, steps)

  else:
    print("find max eig value... ") 
    eig_max_A =  sparse.linalg.eigs(Adj, k=1, return_eigenvectors=False)
    eig_max_A = list(eig_max_A)[0].real 
    
    #eig_max_B = sparse.linalg.eigs(B, k=1, return_eigenvectors=False)
    #eig_max_B = list(eig_max_B)[0].real 
    eig_max_B = eig_max_A 
    print("find max eig value... DONE")
    alpha2 = 1/eig_max_B + 0.02
    print("alpha2",alpha2, eig_max_B)
    I_nXsteps = sparse.identity(n*steps, dtype='int')
    I_nXsteps = scipy.sparse.csc_matrix(I_nXsteps)
    print("taking inverse...")
    W2 = sparse.linalg.inv(I_nXsteps  - alpha2*B)
    W2 = W2*(alpha2*B)**10
    print("taking inverse... DONE")
    W2 = Y.T * W2*X
    C2 = W2.dot(np.ones(n))
    
    for i in C2:
      print(i)
      if i <0:
        raise ValueError("matrix inverse did not give correct result")

    central_nodes = sorted(zip(range(n), C2), key=lambda x:x[1], reverse=True)
    
    for node, cen in central_nodes[:300]:
      if node not in labelled_nodes:
        if graph.degree(node)  <=100:
          print(node, graph.node[node]["community"], "degree", graph.degree(node))
      else:
        if graph.degree(node)  <=-50:
          print(node, graph.node[node]["community"], "degree", graph.degree(node), "labelled node")
        
def draw_graph(graph):
  pos = graphviz_layout(graph, prog='dot')
  
  nx.draw(graph, pos,  node_color='white', node_size=400, arrows=False,with_labels=True)
  plt.show()
  


def extended_star_graph(n,m):
  ''' Return graph on n*m+1 vertices
  '''
  
  G = nx.complete_bipartite_graph(1,n)
  
  for j in range(1,m):
    for i in range(1,n+1):
      G.add_edge(i + (j-1)*n,i + j*n)

  return G
  
  
def star_path_star_graph(n, add_nodes):
  
  
  star1 = nx.complete_bipartite_graph(1,n)
  star2 = nx.complete_bipartite_graph(1,n)
  mapping = dict(zip(range(n+1), range(n+1, 2*n+2)))
  star2  = nx.relabel_nodes(star2, mapping)
  print star1.nodes()
  print star2.nodes()
  graph = nx.union(star1, star2)
  #path from n -->2n + 1 --> 2n + 2 --> .. --> 2n + add_nodes 
  
  if add_nodes:
    path_graph = nx.path_graph(add_nodes)
    mapping = dict(zip(range(add_nodes), range(2*(n+1), 2*(n+1) + add_nodes)))
    path_graph = nx.relabel_nodes(path_graph, mapping)
    graph = nx.union(graph, path_graph)
    graph.add_edge(n,2*(n+1))
    graph.add_edge(2*(n+1) + add_nodes -1, 2*n + 1)
    draw_graph(graph)
  else:
    graph.add_edge(n, 2*n+1)
  #draw_graph(graph)
  centrality = nx.katz_centrality(graph,1/2.5758-0.01, normalized=True)
  for n,c in sorted(centrality.items()):
     print("%d %0.2f"%(n,c))
  return graph
   
   
def read_SNAP_graph(graphfile, source):
  """ Return twitter graph. Edge (u,v) is v follows u 
  This follows the model that a node sends information to it's followers"""
  
  if source == 'twitter':
    edges = np.genfromtxt(graphfile, dtype='int')
    
    graph = nx.DiGraph()
    
    for u,v in edges:
      if u != v:    
        graph.add_edge(v,u)

        
    A = nx.adjacency_matrix(graph)
    scipy.io.savemat('twitter.mat',{'A':A})
    print("graph weakly connected?", nx.is_weakly_connected(graph))
  elif source == 'fb':
    edges = np.genfromtxt(graphfile, usecols=(0,1), dtype='int')
    
    graph = nx.Graph()
    for u,v in edges:
      if u != v:
        graph.add_edge(u,v)
     
    Adj = nx.adjacency_matrix(graph)
    scipy.io.savemat('facebook.mat',{'A':Adj})
    print("num con comps", nx.number_connected_components(graph))
  
  elif source == 'friendster':
    edges = np.genfromtxt(graphfile, delimiter=",", dtype='int')
    graph = nx.Graph()
    for u,v in edges:
      if u != v:
        graph.add_edge(u,v)
    print graph.nodes()[1:10]
    Adj = nx.adjacency_matrix(graph)
    scipy.io.savemat('friendstar.mat',{'A':Adj})
    print("num con comps", nx.number_connected_components(graph))
    
  return graph
      
if __name__ == '__main__':
  #graphfile = "/home/hushiji/Research/centrality/Data/email-Eu-core.txt"
  #labelfile = "/home/hushiji/Research/centrality/Data/email-Eu-core-department-labels.txt"
  
  #graph = read_graph(graphfile, labelfile)
  
  #graph = nx.karate_club_graph()
  #graph = nx.star_graph(30)
  #graph = extended_star_graph(5, 25)
  #graph = star_path_star_graph(6, 0)
  #A = nx.adjacency_matrix(graph)
  #scipy.io.savemat('star_path_star2.mat',{'A':A})
  
  twitter_file = '/home/hushiji/Research/centrality/Data/twitter_combined.txt'
  fb_file = '/home/hushiji/Research/centrality/Data/facebook-links.txt'
  friendster_file = '/home/hushiji/Research/centrality/Data/Friendster-dataset/data/edges.csv'
  graph = read_SNAP_graph(friendster_file, 'friendster')
  '''
  #draw_graph(graph)
  
  steps = 3
  print('diameter',nx.diameter(graph))
  num_labelled_nodes = 4
  #_labelled_nodes = random.sample(graph.nodes(), num_labelled_nodes)
  #lab_nodes2 = [i for i in _labelled_nodes if i >=1*5]
  #_labelled_nodes = lab_nodes2

  _labelled_nodes = [0]
 
  rank_nodes(graph, steps, _labelled_nodes)
  '''
  
  '''
  for i in graph.nodes():
    _labelled_nodes = [i]
    #community_predict = 0
    #com_labelled_nodes = [i for i in _labelled_nodes if graph.node[i]["community"] == community_predict]
    #print(_labelled_nodes)
    rank_nodes(graph, steps, _labelled_nodes)
    #rank_nodes(graph, steps, com_labelled_nodes)
 '''
