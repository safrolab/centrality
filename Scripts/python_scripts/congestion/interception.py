""" Compute number of unique particles a node intercepts from s to t. 
write counter to file
"""

import networkx as nx
import os

def get_counter(graph, walkfile):
    myfile = open(walkfile, 'r')
    counter = dict.fromkeys(graph.nodes(), 0)
    counter2 = dict.fromkeys(graph.nodes(), 0)
    num_walks = 0
    for line in myfile:
        num_walks += 1
        line = line.split()
        nodes = [int(node) for node in line]
        node_set = set(nodes)
        for node in node_set:
            counter[node] += 1
        for node in nodes:
            counter2[node] += 1
    myfile.close()
    scale = 1.0/num_walks
    for node in counter2:
        counter2[node] *= scale
    return counter2
        
def counter_to_file(counter, outdir, filetag):
    myfile = open(outdir + 'counter' + filetag, 'w')
    for node in sorted(counter):
        myfile.write(str(counter[node]) + '\n')
    myfile.close()

     
def experiment(graph):
    # read walk files
    # increment counter
    data_dir = 'pre_data/example/randomwalks/'
    outdir = 'post_data/example/randomwalks/'
    file_nos = []
    for myfile in os.listdir(data_dir):
        if myfile.endswith(".txt"):
            if myfile[:len('randomWalks')] == 'randomWalks':
                file_no = myfile[len('randomWalks'):-4]
                file_no = [int(i) for i in file_no.replace('_', ' ').split()]
                iratio, scenario = file_no
                file_nos.append((iratio, scenario))
    for pair in file_nos:
        ratio, scene = pair
        filetag = str(ratio) + '_' + str(scene) + '.txt'
        walkfile = (data_dir + 'randomWalks' + filetag)
        counter  = get_counter(graph, walkfile)
        counter_to_file(counter, outdir, filetag)

    
if __name__ == '__main__':
    graph = nx.davis_southern_women_graph()
    graph = nx.DiGraph(graph)
    #graphfile = '../../data/p2p-Gnutella08.txt'
    #graphname = 'p2p-Gnutella08'
    graphname = 'example'
    walktype = 'random'
    #graph = nx.read_edgelist(graphfile, nodetype=int, create_using=nx.DiGraph())
    graph = max(nx.weakly_connected_component_subgraphs(graph), key = len)
    graph = nx.convert_node_labels_to_integers(graph, first_label = 0)
    experiment(graph)
