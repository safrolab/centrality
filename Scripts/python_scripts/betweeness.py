import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pygraphviz
import random
from networkx.drawing.nx_agraph import graphviz_layout

class Queue:
  def __init__(self):
    self.in_stack = []
    self.out_stack = []
  def push(self, obj):
    self.in_stack.append(obj)
  def pop(self):
    if not self.out_stack:
      while self.in_stack:
        self.out_stack.append(self.in_stack.pop())
    return self.out_stack.pop()
    
  def is_empty(self):
    
    if not self.in_stack and not self.out_stack:
      return True
    else:
      return False 
  
def _netX_single_source_shortest_path_basic(G, s):
    S = []
    P = {}
    for v in G:
        P[v] = []
    sigma = dict.fromkeys(G, 0.0)    # sigma[v]=0 for v in G
    D = {}
    sigma[s] = 1.0
    D[s] = 0
    Q = [s]
    while Q:   # use BFS to find shortest paths
        v = Q.pop(0)
        S.append(v)
        Dv = D[v]
        sigmav = sigma[v]
        for w in G[v]:
            if w not in D:
                Q.append(w)
                D[w] = Dv + 1
            if D[w] == Dv + 1:   # this is a shortest path, count paths
                sigma[w] += sigmav
                P[w].append(v)  # predecessors
    return S, P, sigma
    
    
def _single_source_shortest_path_basic(G, G_n_soc_nodes, s, steps, install_units):
    #install_units = dict
    #s = (node, soc_level) 
    S = []
    P = {}

    for v in G_n_soc_nodes: #G:
        P[v] = []
    #sigma = dict.fromkeys(G, 0.0)    # sigma[v]=0 for v in G
    sigma = dict.fromkeys(G_n_soc_nodes, 0.0)# sigma[v]=0 for v in G_n_soc_nodes
    D = {}
    sigma[s] = 1.0
    D[s] = 0
    #Q = [s]
    Q = Queue()
    Q.push(s)
    while not Q.is_empty():   # use BFS to find shortest paths
        #v = Q.pop(0)
        v = Q.pop() # v = (node, soc_level)
        S.append(v)
        Dv = D[v]
        sigmav = sigma[v]
        node_v, soc_v = v
        if soc_v != 'terminal':
            for node_w in G[node_v]:
                if node_w != s[0]: # dont return to source node
                    if install_units[node_w]:
                        #recharge soc
                        current_node = (node_w, steps - 1) #full soc  = steps - 1
                    else:
                        if soc_v > 0:
                            current_node = (node_w, soc_v - 1) #full soc  = steps - 1
                        else:
                            current_node = None
                    if current_node:
                        if current_node not in D:
                            Q.push(current_node)
                            D[current_node] = Dv + 1
                        if D[current_node] == Dv + 1: # this is a shortest path, count paths
                            sigma[current_node] += sigmav
                            P[current_node].append(v)  # predecessors\
            current_node = (node_v, 'terminal')
            if current_node not in D:
                Q.push(current_node)
                D[current_node] = Dv + 1
            if D[current_node] == Dv + 1: # this is a shortest path, count paths
                sigma[current_node] += sigmav
                P[current_node].append(v)  # predecessors

    return S, P, sigma, D

def _netX_accumulate_basic(betweenness, S, P, sigma, s):
    delta = dict.fromkeys(S, 0)
    while S:
        w = S.pop()
        
        coeff = (1.0 + delta[w]) / sigma[w]
        for v in P[w]:
            delta[v] += sigma[v] * coeff
        if w != s:
            betweenness[w] += delta[w]
    return betweenness
    

def _netX_accumulate_endpoints(betweenness, S, P, sigma, s):
    betweenness[s] += len(S) - 1
    delta = dict.fromkeys(S, 0)
    while S:
        w = S.pop()
        coeff = (1.0 + delta[w]) / sigma[w]
        for v in P[w]:
            delta[v] += sigma[v] * coeff
        if w != s:
            betweenness[w] += delta[w] + 1
    return betweenness
    
    
def _accumulate_basic(betweenness, S, P, sigma, s, D):

    contribute_to_bc = {}
    #terminal_predecessor = {}
    #for node in S:
        #terminal_predecessor[node] = False
    for node in S:
        node_v, soc = node
        if soc == 'terminal':
            contribute_to_bc[node] = True
            #for v in P[node]:
            #    terminal_predecessor[v] = True
        else:
            contribute_to_bc[node] = False
    delta = dict.fromkeys(S, 0)
    
    btn_s = 0
    while S:
        w = S.pop()

        if contribute_to_bc[w]:
            coeff = (1.0 + delta[w]) / sigma[w]
            coeff2 = delta[w]/sigma[w]
            node_w, soc_w = w
            if soc_w == 'terminal':
                btn_s += 1
            for v in P[w]:
                contribute_to_bc[v] = True
                if soc_w != 'terminal':
                    delta[v] += sigma[v] * coeff2
                    #if not terminal_predecessor[v]:
                    #    delta[v] += sigma[v] * coeff2
                    #    print 'here'
                    #else:
                        #delta[v] += sigma[v] * coeff
                    #    delta[v] += sigma[v] * coeff2
                    #    #print v, w, delta[v] , delta[w]
                else:
                    #sigma[v] = sigma[w]
                    delta[v] += sigma[v] * coeff
            if w != s:
                betweenness[w] += delta[w]
    betweenness[s] +=  btn_s -1 #number of times s is a source
    return betweenness
    
def soc_betweenness_centrality(G, soc_nodes, steps, install_units, k=None, 
                           normalized=True, endpoints=False, seed=None):

    #betweenness = dict.fromkeys(G, 0.0)  # b[v]=0 for v in G
    betweenness = dict.fromkeys(soc_nodes, 0.0)  # b[v]=0 for v in G
    if k is None:
        nodes = G.nodes()
    else:
        random.seed(seed)
        nodes = random.sample(G.nodes(), k)
    for node_s in nodes:
        print("node_s", node_s)
        # single source shortest paths
        # use BFS
        #S, P, sigma = _single_source_shortest_path_basic(G, s)
        s = (node_s, steps-1) #start at full soc
        S, P, sigma, D = _single_source_shortest_path_basic(G, soc_nodes, s, steps,
                                                         install_units)

        # accumulation
        #if endpoints:
        #    betweenness = _accumulate_endpoints(betweenness, S, P, sigma, s)
        #else:
        betweenness = _accumulate_basic(betweenness, S, P, sigma, s, D)
    # rescaling
    #betweenness = _rescale(betweenness, len(G),
    #                       normalized=normalized,
    #                       directed=G.is_directed(),
    #                       k=k)
    return betweenness


def betweenness_centrality(G, soc_nodes, steps, install_units):
    soc_betweenness = soc_betweenness_centrality(
        G, soc_nodes, steps, install_units, k=None, normalized=True,
        endpoints=False, seed=None
        )
    #for node in sorted(soc_betweenness):
    #    print node, soc_betweenness[node]
    betweenness = {}
    for node, soc_level in soc_betweenness:
        if node not in betweenness:
            betweenness[node] = soc_betweenness[(node, soc_level)]
        else:
            betweenness[node] += soc_betweenness[(node, soc_level)]
    for v in betweenness:
        betweenness[v] *= 1.0/2.0 #rescale for undirected graphs
    return betweenness

def get_coordinates(cordfile):
    
    data = np.genfromtxt(cordfile)
    data = list(data)
    n = len(data)
    #x = [cord for k, cord in enumerate(data) if k %2 == 1]
    #y = [cord for k, cord in enumerate(data) if k %2 == 0]
    print(n)
    x = data[:int(n/2)]
    y = data[int(n/2):]
    
    return x, y


def shortest_path_subgraph(G, s):
    S, P, sigma = _netX_single_source_shortest_path_basic(G, s)
    terminal_nodes = {}
    for node in G.nodes():
        terminal_nodes[node] = False
    
    terminal_nodes[4] = True
    print(S)
    print(P[4])
    while len(S) > 0:
        node = S.pop()
        if terminal_nodes[node]:
            for v in P[node]:
                terminal_nodes[v] = True
    for node in terminal_nodes:
        if terminal_nodes[node]:
            print(node, nx.shortest_path_length(G, s, node))
    
def draw_graph(graph, mybetweenness, standard_betweenness, cordfile):

    m_betweenness = []
    s_betweenness = []
    for node in sorted(graph.nodes()):
        m_betweenness.append(mybetweenness[node])
        s_betweenness.append(standard_betweenness[node])
    node_sizes = []
    for node in sorted(graph.nodes()):
        node_sizes.append(int(mybetweenness[node])/2000)
    #pos = graphviz_layout(graph, prog='sfdp')
    x, y = get_coordinates(cordfile)   
    pos = {}
    for node in graph.nodes():
        pos[node] = [x[node-1], y[node-1]]

    #nx.draw(graph, pos, node_size = node_sizes, node_color=m_betweenness)
    nodes = nx.draw_networkx_nodes(G,pos,node_color=m_betweenness, node_size =80,
                cmap=plt.cm.autumn_r, linewidths=0, with_labels=False)
    edges = nx.draw_networkx_edges(G,pos,edge_color='gray',width=1)
    plt.colorbar(nodes)
    plt.axis('off') 
    
    
    plt.savefig("mybetweenness.eps") 
    #plt.show()
    
    node_sizes = []
    for node in sorted(graph.nodes()):
        node_sizes.append(int(standard_betweenness[node])/2000)
        
  
    plt.clf()
    
    #nx.draw(graph, pos, node_size =80, node_color=s_betweenness
    #            ,linewidths=0, cmap=plt.cm.autumn_r, edge_color='grey', with_labels=False)
    
    nodes = nx.draw_networkx_nodes(G,pos,node_color=s_betweenness, node_size =80,
                cmap=plt.cm.autumn_r, linewidths=0, with_labels=False)
    edges = nx.draw_networkx_edges(G,pos,edge_color='gray',width=1)
    plt.colorbar(nodes)
    plt.axis('off')                         
                               
    plt.savefig("standard_betweenness.eps") 
    #plt.show()

def draw_debug_graph(graphfile, cordfile):
    #G = nx.read_edgelist(graphfile, nodetype=int)
    G = nx.Graph()
    edges = np.genfromtxt(graphfile, dtype='int')
    
    for u,v in edges:
        G.add_edge(u,v)
    x, y = get_coordinates(cordfile)   

    pos = {}
    for node in G.nodes():
        pos[node] = [x[node-1], y[node-1]]
    
    nx.draw(G, pos, node_size = 10)
    #plt.plot(x,y, 'o')
    plt.show()

def debug():
    G = nx.karate_club_graph()
    #G = nx.grid_2d_graph(5,5)
    G = nx.convert_node_labels_to_integers(G)
    #G = nx.Graph()
    #G.add_edges_from([(0,1), (0,2), (2,1), (1,4), (4,5), (4,3), (5,3)])
    #shortest_path_subgraph(G, 0)
    #nx.draw(G, with_labels=True)
    #plt.show()

    
    graphfile = '/home/hushiji/Research/centrality/Scripts/data/minesota_graph.txt'
    cordfile = '/home/hushiji/Research/centrality/Scripts/data/minnesota_coord.mtx'
    
   
    """
    G = nx.read_edgelist(graphfile, nodetype=int)
    #draw_cord_graph(graphfile, cordfile)
    #G = nx.cycle_graph(10)
    steps = 2
    G_n_soc_nodes = []
    install_units = {}
    for node in G.nodes():
        install_units[node] = False
        G_n_soc_nodes.append((node, 'terminal'))
        for soc_level in range(steps):
            G_n_soc_nodes.append((node, soc_level))
    
    num_install = int(0.1*nx.number_of_nodes(G))
    install_nodes = random.sample(G.nodes(), num_install)
    #install_nodes = []
    #print nx.neighbors(G, install_nodes[0])
    #install_nodes = G.nodes()
    for node in install_nodes:
        install_units[node] = True
        """
    """
    s = (2,steps-1)
    S, P, sigma, D = _single_source_shortest_path_basic(G, G_n_soc_nodes, s, steps,
                                                    install_units)
    betweenness = dict.fromkeys(G_n_soc_nodes, 0.0)     
    betweenness = _accumulate_basic(betweenness, S, P, sigma, s, D)    
    for node in betweenness:
        if betweenness[node] > 0:
            print node, betweenness[node]  
            
    s = 2
    S, P, sigma = _netX_single_source_shortest_path_basic(G, s)
    betweenness = dict.fromkeys(G.nodes(), 0.0)     
    #betweenness = _netX_accumulate_basic(betweenness, S, P, sigma, s)   
    betweenness =  _netX_accumulate_endpoints(betweenness, S, P, sigma, s)  
    for node in betweenness:
        if betweenness[node] > 0:
            print node, betweenness[node]    
    """                                              

    betweenness = betweenness_centrality(G, G_n_soc_nodes, steps, install_units)
    standard_betweenness = nx.betweenness_centrality(G, normalized=False, endpoints=True)
    btn = sorted([(betweenness[node], node) for node in betweenness], reverse=True)
    btn2 = sorted([(standard_betweenness[node], node) for node in standard_betweenness], reverse=True)
    nodes_1 = [ node for _ , node in btn]
    nodes_2 = [ node for _ , node in btn2]

    
    for i in range(len(nodes_1)):
        node1 = nodes_1[i]
        node2 = nodes_2[i]
        if node1 != node2:
            print  node2, standard_betweenness[node2], node1, betweenness[node1] 


def debug_graphs():
    n = 5
    m = 4
    clique1 = nx.grid_graph([n,n])
    clique1 = nx.convert_node_labels_to_integers(clique1)
    clique2 = nx.grid_graph([n,n])
    clique2 = nx.convert_node_labels_to_integers(clique2)
    path = nx.path_graph(m)
    mapping_path = dict(zip(path.nodes(), range(n**2, n**2 +m)))
    path = nx.relabel_nodes(path, mapping_path)
    mapping2 = dict(zip(clique2.nodes(), range(n**2+m, 2*n**2 + m)))
    clique2 = nx.relabel_nodes(clique2, mapping2)
    G = nx.union(clique1, path)
    G = nx.union(G, clique2)
    G.add_edges_from([(n**2-1, n**2), (n**2+m-1, 2*n**2 + 3)])
    #nx.draw(G)
    #plt.show()
    return G

if __name__ == '__main__':  
    graphfile = '/home/hayato/Research/centrality/Scripts/data/minnesota.mtx'
    cordfile = '/home/hayato/Research/centrality/Scripts/data/minnesota_coord.mtx'
    

    G = nx.read_edgelist(graphfile, nodetype=int)
    #G = nx.karate_club_graph()
    #G = nx.grid_2d_graph(5,5)
    #G = debug_graphs()
    #G = nx.convert_node_labels_to_integers(G)
    steps = 20
    G_n_soc_nodes = []
    install_units = {}
    for node in G.nodes():
        install_units[node] = False
        G_n_soc_nodes.append((node, 'terminal'))
        for soc_level in range(steps):
            G_n_soc_nodes.append((node, soc_level))
    
    num_install = int(0.1*nx.number_of_nodes(G))
    install_nodes = random.sample(G.nodes(), num_install)
    install_nodes = []
    for node in install_nodes:
        install_units[node] = True
    mybetweenness = betweenness_centrality(G, G_n_soc_nodes, steps, install_units)
    #btn = sorted([(mybetweenness[node], node) for node in mybetweenness], reverse=True)
    #for _, node in btn:
    #    print node, mybetweenness[node]
    standard_betweenness = nx.betweenness_centrality(G, normalized=False, endpoints=True)
    draw_graph(G, mybetweenness, standard_betweenness, cordfile)
   
