'''
1. Read graph
2. Read s, t, full_soc and install_nodes
3. Read two centrality files
4. Make plots
'''
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def get_graph():
    graphfile = 'myminnesota_graph.txt'
    graph = nx.read_edgelist(graphfile, nodetype=int)
    return graph

def get_coordinates(cordfile):
    data = np.genfromtxt(cordfile)
    data = list(data)
    n = len(data)
    #x = [cord for k, cord in enumerate(data) if k %2 == 1]
    #y = [cord for k, cord in enumerate(data) if k %2 == 0]
    x = data[:int(n/2)]
    y = data[int(n/2):]
    return x, y


def get_parameters():
    data = np.genfromtxt('s_t_full_soc.txt', dtype=int)
    s, t, full_soc = data
    install_nodes = list(np.genfromtxt('install_nodes.txt', dtype=int))
    return s, t, install_nodes


def get_centrality_scores():
    standard_cen = list(np.genfromtxt('mycentrality_standard.txt'))
    print 'max cen value', max(standard_cen)
    soc_cen = list(np.genfromtxt('mycentrality_SOC.txt'))
    mycen_standard = {}
    mycen_soc = {}
    print len(soc_cen), len(standard_cen)
    for i in range(len(soc_cen)):
        mycen_standard[i] = standard_cen[i]
        mycen_soc[i] = soc_cen[i]
    return mycen_standard, mycen_soc
    


def get_max_connected_comm():
    # original data
    graphfile = '/home/hushiji/Research/centrality/Scripts/data/minnesota.mtx'
    cordfile = '/home/hushiji/Research/centrality/Scripts/data/minnesota_coord.mtx'
    
    graph = nx.read_edgelist(graphfile, nodetype=int)
    x, y = get_coordinates(cordfile)
    pos = {}
    for node in graph.nodes():
        pos[node] = [x[node-1], y[node-1]]
    graph = max(nx.connected_component_subgraphs(graph), key=len)
    newgraph = nx.convert_node_labels_to_integers(graph, first_label=1, ordering='sorted')
    
    # new graph and cord to file
    myfile = open('myminnesota_graph.txt', 'w')
    for u, v in newgraph.edges():
        out = " ".join([str(u), str(v) +'\n', str(v), str(u) + '\n'])
        myfile.write(out)
    myfile.close()
    myfile = open('myminnesota_cord.txt', 'w')
    newPos = {}
    for i, node in enumerate(sorted(graph.nodes()), start=1):
        newPos[i] = pos[node]
    for node in newPos:
        x, y = newPos[node]
        myfile.write(str(node) + ' ' + str(x) + ' ' + str(y) + '\n')
    myfile.close()


def get_pos_from_file(posfile):
    pos = {}
    myfile = open(posfile, 'r')
    for line in myfile:
        line = line.split()
        node, x, y = line
        node, x, y = int(node), float(x), float(y)
        pos[node] = [x, y]
    return pos        


def plot_standardard_cen():
    graph = get_graph()
    s, t, install_nodes = get_parameters()
    mycen_standard, mycen_soc = get_centrality_scores()
    posfile = 'myminnesota_cord.txt'
    
    # plot graph
    standard_cen = []
    for node in sorted(graph.nodes()):
        standard_cen.append(mycen_standard[node-1])
    node_sizes = []

    for node in sorted(graph.nodes()):
        cen  = float(mycen_standard[node - 1])
        if cen <= 0.000001:
            node_sizes.append(10)
        else:
            node_sizes.append(100)
    pos = get_pos_from_file(posfile)
    nodes = nx.draw_networkx_nodes(graph,
                                    pos,
                                    node_color=standard_cen,
                                    node_size =node_sizes,
                                    #cmap=plt.cm.Blues,
                                    cmap=plt.cm.autumn_r,
                                    linewidths=0,
                                    with_labels=False)
    s_t_graph = nx.Graph()
    s_t_graph.add_node(s)
    s_t_graph.add_node(t)
    s_t_pos = {}
    s_t_pos[s] = pos[s]
    s_t_pos[t] = pos[t]
    nodes3 = nx.draw_networkx_nodes(s_t_graph,
                                    s_t_pos,
                                    node_color='black',
                                    node_size =60)
    edges = nx.draw_networkx_edges(graph,pos,edge_color='gray',width=1)
    plt.colorbar(nodes)
    plt.axis('off') 
    plt.show()


def plot_soc_centrality():
    graph = get_graph()
    s, t, install_nodes = get_parameters()
    shortestDistance = nx.shortest_path_length(graph, source=s, target=t)
    print "shortest distance from %i --> %i is %i" %(s, t, shortestDistance)

    _, mycen_soc = get_centrality_scores()
    posfile = 'myminnesota_cord.txt'
    
    # plot graph
    install_graph = nx.Graph()
    for node in install_nodes:
        install_graph.add_node(node)
    soc_cen = []
    for node in sorted(graph.nodes()):
        soc_cen.append(mycen_soc[node-1])

    node_sizes = []
    for node in sorted(graph.nodes()):
        cen  = float(mycen_soc[node - 1])
        if cen <= 0.000001:
            node_sizes.append(10)
        else:
            node_sizes.append(100)
    pos = get_pos_from_file(posfile)
    
    nodes = nx.draw_networkx_nodes(graph,
                                    pos,
                                    node_color=soc_cen,
                                    node_size =node_sizes,
                                    #cmap=plt.cm.Blues,
                                    cmap=plt.cm.autumn_r,
                                    linewidths=0,
                                    with_labels=False)
    pos2 = {}
    for node in install_nodes:
        pos2[node] = pos[node]
    btn2 = [soc_cen[node-1] for node in install_graph.nodes()]
    #size2 = [node_sizes[node-1] for node in install_graph.nodes()]
    size2 = [60 for node in install_graph.nodes()]
    nodes2 = nx.draw_networkx_nodes(install_graph,
                                    pos2,
                                    node_color=btn2,
                                    node_size =size2,
                                    #cmap=plt.cm.Blues,
                                    cmap=plt.cm.autumn_r,
                                    vmin=min(soc_cen),
                                    vmax=max(soc_cen),
                                    linewidths=2)

    nodes2.set_edgecolor('b')
    
    s_t_graph = nx.Graph()
    s_t_graph.add_node(s)
    s_t_graph.add_node(t)
    s_t_pos = {}
    s_t_pos[s] = pos[s]
    s_t_pos[t] = pos[t]
    nodes3 = nx.draw_networkx_nodes(s_t_graph,
                                    s_t_pos,
                                    node_color='black',
                                    node_size =60)
    edges = nx.draw_networkx_edges(graph,pos,edge_color='gray',width=1)
    plt.colorbar(nodes)
    plt.axis('off') 
    plt.show()

def make_plots():
    graph = get_graph()
    s, t, install_nodes = get_parameters()
    mycen_standard, mycen_soc = get_centrality_scores()
    posfile = 'myminnesota_cord.txt'
    
    # plot graph
    install_graph = nx.Graph()
    for node in install_nodes:
        install_graph.add_node(node)
    standard_cen = []
    soc_cen = []
    for node in sorted(graph.nodes()):
        soc_cen.append(mycen_soc[node-1])
        standard_cen.append(mycen_standard[node-1])
    p1 = np.percentile(soc_cen, 50)
    p2 = np.percentile(soc_cen, 75)
    p3 = np.percentile(soc_cen, 90)
    p4 = np.percentile(soc_cen, 95)
    node_sizes = []
    '''
    for node in sorted(graph.nodes()):
        cen  = int(mycen_standard[node - 1])
        if cen < p1:
            node_sizes.append(60)
        elif cen < p2:
            node_sizes.append(60)
        elif cen < p3:
            node_sizes.append(60)
        elif cen < p4:
            node_sizes.append(60)
        else:
            node_sizes.append(60)
    '''
    for node in sorted(graph.nodes()):
        cen  = float(mycen_standard[node - 1])
        if cen <= 0.000001:
            node_sizes.append(10)
        else:
            node_sizes.append(100)
    pos = get_pos_from_file(posfile)
    nodes = nx.draw_networkx_nodes(graph,
                                    pos,
                                    node_color=standard_cen,
                                    node_size =node_sizes,
                                    #cmap=plt.cm.Blues,
                                    cmap=plt.cm.autumn_r,
                                    linewidths=0,
                                    with_labels=False)
    pos2 = {}
    for node in install_nodes:
        pos2[node] = pos[node]
    btn2 = [mycen_standard[node] for node in install_graph.nodes()]
    #size2 = [node_sizes[node-1] for node in install_graph.nodes()]
    size2 = [60 for node in install_graph.nodes()]
    nodes2 = nx.draw_networkx_nodes(install_graph,
                                    pos2,
                                    node_color=btn2,
                                    node_size =size2,
                                    #cmap=plt.cm.Blues,
                                    cmap=plt.cm.autumn_r,
                                    vmin=min(mycen_standard),
                                    vmax=max(mycen_standard),
                                    linewidths=2)

    nodes2.set_edgecolor('b')
    edges = nx.draw_networkx_edges(graph,pos,edge_color='gray',width=1)
    plt.colorbar(nodes)
    plt.axis('off') 
    plt.show()

if __name__ == '__main__':
    # note: minnesota graph nodes start at 1 because we use in matlab too
    #make_plots()
    #get_max_connected_comm()
    plot_standardard_cen()
    plot_soc_centrality()


