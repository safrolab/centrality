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

    for node in S:
        node_v, soc = node
        if soc == 'terminal':
            contribute_to_bc[node] = True
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
                else:
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
    
def draw_graph(graph, install_nodes, mybetweenness, standard_betweenness, cordfile):
    install_graph = nx.Graph()
    for node in install_nodes:
        install_graph.add_node(node)
        

    if cordfile:
        m_betweenness = []
        s_betweenness = []
        for node in sorted(graph.nodes()):
            m_betweenness.append(mybetweenness[node])
            s_betweenness.append(standard_betweenness[node])
        p1 = np.percentile(m_betweenness, 50)
        p2 = np.percentile(m_betweenness, 75)
        p3 = np.percentile(m_betweenness, 90)
        p4 = np.percentile(m_betweenness, 95)
        node_sizes = []
        for node in sorted(graph.nodes()):
            cen  = int(mybetweenness[node])
            if cen < p1:
                node_sizes.append(20)
            elif cen < p2:
                node_sizes.append(30)
            elif cen < p3:
                node_sizes.append(40)
            elif cen < p4:
                node_sizes.append(80)
            else:
                node_sizes.append(100)
                #node_sizes.append(int(mybetweenness[node])/2000)
        #pos = graphviz_layout(graph, prog='sfdp')
        x, y = get_coordinates(cordfile)   
        pos = {}
        for node in graph.nodes():
            pos[node] = [x[node-1], y[node-1]]

         
        #nx.draw(graph, pos, node_size = node_sizes, node_color=m_betweenness)
        nodes = nx.draw_networkx_nodes(G,pos,node_color=m_betweenness, node_size =node_sizes,
                    cmap=plt.cm.Blues, linewidths=0, with_labels=False)
        pos2 = {}
        for node in install_nodes:
            pos2[node] = pos[node]
        btn2 = [mybetweenness[node] for node in install_graph.nodes()]
        size2 = [node_sizes[node-1] for node in install_graph.nodes()]
        nodes2 = nx.draw_networkx_nodes(install_graph, pos2,node_color=btn2, node_size =size2, cmap=plt.cm.Blues, vmin=min(m_betweenness), vmax=max(m_betweenness),  linewidths=0.8)

        nodes2.set_edgecolor('r')
        edges = nx.draw_networkx_edges(G,pos,edge_color='gray',width=1)
        plt.colorbar(nodes)
        plt.axis('off') 
        
        
        #plt.savefig("_delete_mybetweenness.eps") 
        plt.show()
        '''
        p1 = np.percentile(s_betweenness, 20)
        p2 = np.percentile(s_betweenness, 40)
        p3 = np.percentile(s_betweenness, 60)
        p4 = np.percentile(s_betweenness, 80)
        node_sizes = []
        for node in sorted(graph.nodes()):
            cen  = int(standard_betweenness[node])
            if cen < p1:
                node_sizes.append(10)
            elif cen < p2:
                node_sizes.append(20)
            elif cen < p3:
                node_sizes.append(60)
            elif cen < p4:
                node_sizes.append(150)
            else:
                node_sizes.append(180)
      
        plt.clf()
        
        #nx.draw(graph, pos, node_size =80, node_color=s_betweenness
        #            ,linewidths=0, cmap=plt.cm.autumn_r, edge_color='grey', with_labels=False)
        
        nodes = nx.draw_networkx_nodes(G,pos,node_color=s_betweenness, node_size =node_sizes,
                    cmap=plt.cm.Blues, linewidths=0, with_labels=False)
        nodes2 = nx.draw_networkx_nodes(install_graph, pos2,node_color=btn2, node_size =100, cmap=plt.cm.Blues, vmin=min(m_betweenness), vmax=max(m_betweenness),  linewidths=2)

        nodes2.set_edgecolor('r')
        #labels = nx.draw_networkx_labels(G,pos)
        edges = nx.draw_networkx_edges(G,pos,edge_color='gray',width=1)
        plt.colorbar(nodes)
                                   
        #plt.savefig("standard_betweenness.eps") 
        plt.show()
        '''
    else:
        m_betweenness = []
        s_betweenness = []
        for node in sorted(graph.nodes()):
            m_betweenness.append(mybetweenness[node])
            s_betweenness.append(standard_betweenness[node])

        pos = graphviz_layout(graph, prog='sfdp')
        pos2 = {}
        for node in install_nodes:
            pos2[node] = pos[node]
        btn2 = [mybetweenness[node] for node in install_graph.nodes()]

        #plt.figure(figsize=(25,18))
        nodes = nx.draw_networkx_nodes(G,pos,node_color=m_betweenness, node_size =100,
                    cmap=plt.cm.Blues, linewidths=0.2)
        #nodes2 = nx.draw_networkx_nodes(install_graph, pos2,node_color=btn2, node_size =100,
          #          cmap=plt.cm.Blues, vmin=min(m_betweenness), vmax=max(m_betweenness),  linewidths=2)

        #nodes2.set_edgecolor('r')
        #labels = nx.draw_networkx_labels(G,pos)
        edges = nx.draw_networkx_edges(G,pos,edge_color='gray',width=0.5)
        plt.colorbar(nodes)
        plt.axis('off') 
        

        plt.savefig("exp_cen_20.eps") 
        #plt.show()

        plt.clf()
        
        nodes = nx.draw_networkx_nodes(G,pos,node_color=s_betweenness, node_size =100,
                    cmap=plt.cm.Blues, linewidths=0.2)
        edges = nx.draw_networkx_edges(G,pos,edge_color='gray',width=1)
        plt.colorbar(nodes)
        plt.axis('off')                         
                                   
        #plt.savefig("standard_betweenness.eps") 
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

def normalize(mybetweeness):
    scale = 1.0/1000
    
    for v in mybetweenness:
        mybetweenness[v] *= scale
    return mybetweenness
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



def test_cen_values():
    myfile = open('minnesota_20_vs_standard.txt')
    
    mycen = []
    s_cen = []
    for line in myfile:
        line = line.split()
        node = line[0]
        mycen.append(float(line[1]))
        s_cen.append(float(line[2]))
    m_norm = [float(i)/max(mycen) for i in mycen]
    s_norm = [float(i)/max(s_cen) for i in s_cen]
    plt.histfit(m_norm, bins=100)
    plt.show()
    #plt.plot(m_norm, s_norm, 'o')
    #plt.show()
    
def expected_btn_centrality(graph, G_n_soc_nodes, steps, k):
    
    install_units = {}
    exp_cen = dict.fromkeys(graph.nodes(), 0.0) 
    for node in graph.nodes():
        install_units[node] = False
        
    for _ in range(1000):
      install_nodes = random.sample(graph.nodes(),k)
      for node in install_nodes:
        install_units[node] = True
      mybetweenness = betweenness_centrality(G, G_n_soc_nodes, steps, install_units)
      for u in graph.nodes():
        exp_cen[u] += mybetweenness[u]
      for node in install_nodes:
        install_units[node] = False
      
    return exp_cen

    
if __name__ == '__main__':  
    graphfile = '/home/hushiji/Research/centrality/Scripts/data/minnesota.mtx'
    cordfile = '/home/hushiji/Research/centrality/Scripts/data/minnesota_coord.mtx'
    #test_cen_values()
    G = nx.read_edgelist(graphfile, nodetype=int)

    #G = nx.karate_club_graph()
    #G = nx.grid_2d_graph(5,5)
    #G = debug_graphs()
    #cordfile = None
    #G = nx.convert_node_labels_to_integers(G)
    steps = 10
    G_n_soc_nodes = []
    install_units = {}
    for node in G.nodes():
        install_units[node] = False
        G_n_soc_nodes.append((node, 'terminal'))
        for soc_level in range(steps):
            G_n_soc_nodes.append((node, soc_level))
    
    num_install = int(0.05*nx.number_of_nodes(G))
    install_nodes = random.sample(G.nodes(), num_install)
    #install_nodes = []
    #install_nodes = [26]
    #install_nodes = [45,16]
    #install_nodes = [45,16,26]
    #install_nodes = [24,53]
    #install_nodes = [24,53, 44, 32,31, 47,3, 18, 15, 2]
    #install_nodes = [44, 32,31, 47,3, 18, 15, 2]
    #install_nodes = [33, 36, 46, 43, 7,14, 4, 17]

    for node in install_nodes:
        install_units[node] = True
    mybetweenness = betweenness_centrality(G, G_n_soc_nodes, steps, install_units)
    #btn = sorted([(mybetweenness[node], node) for node in mybetweenness], reverse=True)
    #for _, node in btn:
    #    print node, mybetweenness[node]

    standard_betweenness = nx.betweenness_centrality(G, normalized=False, endpoints=True)
    #mybetweenness =  expected_btn_centrality(G, G_n_soc_nodes, steps,5)
    mybetweenness = normalize(mybetweenness)
    #s_btn = [standard_betweenness[i] for i in standard_betweenness]
    #m_btn = [mybetweenness[i] for i in standard_betweenness]
    #plt.plot(s_btn, m_btn, 'o')
    #plt.show()
    #draw_graph(G, install_nodes, standard_betweenness, standard_betweenness, cordfile)
    draw_graph(G, install_nodes, mybetweenness, standard_betweenness, cordfile)
   
