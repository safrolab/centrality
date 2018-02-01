"""Compute congestion in graph from feasible walk written to file

"""
import networkx as nx
import random
import math
import scipy.stats as sc
import sys
sys.path.insert(0, '/home/hushiji/Research/centrality/Scripts/python_scripts/')
import betweenness as soc
import BC_fixed_source as standard_fixed_source
import os
import numpy as np


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

    def len(self):
        return len(self.in_stack) + len(self.out_stack)

    def is_empty(self):
        if not self.in_stack and not self.out_stack:
            return True
        else:
            return False

      
def read_feasible_walks(filename):
    myfile = open(filename, 'r')
    walk_id = 0
    feasible_walks = {}
    feasible_walks_source = {}
    for line in myfile:
        line = line.split()
        line = [int(i) for i in line]
        feasible_walks[walk_id] = line
        walk_id += 1
        source = line[-1]
        if source in feasible_walks_source:
            feasible_walks_source[source].append(line)
        else:
            feasible_walks_source[source] = [line]
    for source in feasible_walks_source:
        random.shuffle(feasible_walks_source[source])
    return feasible_walks, feasible_walks_source


def get_install_dict(graph, filename):
    install_nodes = np.genfromtxt(filename, dtype='int')
    install_nodes = install_nodes.tolist()
    install_dict = dict.fromkeys(graph.nodes(), False)
    if type(install_nodes) == list:
        for node in install_nodes:
            install_dict[node] = True
    else:
        install_dict[install_nodes] = True  # 1 install node which is int
        install_nodes = [install_nodes]
    return install_dict, install_nodes


def get_source_nodes(graph, filename):
    return list(np.genfromtxt(filename, dtype='int'))


def particle_time_step_fixed_source(graph,
                                    occupied_streets,
                                    Routes,
                                    max_counter,
                                    average_counter):
    """Perform a time step of particle simulation.

    At each step, a single particle in each occupied node, moves to a
    neighboring node.
    """

    for street in occupied_streets.keys():
        route_queue = occupied_streets[street]
        route_id = route_queue.pop()
        next_step = Routes[route_id].pop()
        if len(Routes[route_id]) == 0:  # Arrived at target
            del Routes[route_id]
        else:
            if next_step in occupied_streets:
                occupied_streets[next_step].push(route_id)
                node_congestion = occupied_streets[next_step].len()
                average_counter[next_step] += node_congestion
                if max_counter[next_step] < node_congestion:
                    max_counter[next_step] = node_congestion
            else:
                occupied_streets[next_step] = Queue()
                occupied_streets[next_step].push(route_id)
                average_counter[next_step] += 1
                max_counter[next_step] = max(max_counter[next_step], 1)
        if route_queue.len() == 0:
            del occupied_streets[street]      
    return occupied_streets, Routes, max_counter, average_counter


def particle_birth_fixed_source(graph,
                                occupied_streets,
                                Routes,
                                max_counter,
                                average_counter,
                                num_new_routes,
                                feasible_walks,
                                feasible_walks_source,
                                used_walk_indx,
                                num_feasible_walks,
                                num_avail_source,
                                birth_type):
    if birth_type == 'walk_at_random':
        max_route_id = Routes['max_id']
        for i in range(num_new_routes):
            if used_walk_indx >= num_feasible_walks -1:
                break
            else:
                used_walk_indx += 1
                walk = feasible_walks[used_walk_indx]
                max_route_id += 1
                Routes['max_id'] = max_route_id
                Routes[max_route_id] = walk
                source = walk[-1]
                if source in occupied_streets:
                    occupied_streets[source].push(max_route_id)
                    node_congestion = occupied_streets[source].len()
                    average_counter[source] += node_congestion
                    if max_counter[source] < node_congestion:
                        max_counter[source] = node_congestion
                else:
                    occupied_streets[source] = Queue()
                    occupied_streets[source].push(max_route_id)
                    average_counter[source] += 1
                    max_counter[source] = max(max_counter[source], 1)
    elif birth_type == 'random_source':
        max_route_id = Routes['max_id']
        start_nodes = random.sample(feasible_walks_source.keys(),
                                    min(num_avail_source, num_new_routes))
        for source in start_nodes:
            if used_walk_indx >= num_feasible_walks -1:
                break
            else:
                if source in feasible_walks_source: 
                    used_walk_indx += 1
                    walk = feasible_walks_source[source].pop()
                    #walk = random.choice(feasible_walks_source[source])
                    if len(feasible_walks_source[source]) == 0:
                        del feasible_walks_source[source]
                        num_avail_source -= 1
                    max_route_id += 1
                    Routes['max_id'] = max_route_id
                    Routes[max_route_id] = walk
                    if source in occupied_streets:
                        occupied_streets[source].push(max_route_id)
                        node_congestion = occupied_streets[source].len()
                        average_counter[source] += node_congestion
                        if max_counter[source] < node_congestion:
                            max_counter[source] = node_congestion
                    else:
                        occupied_streets[source] = Queue()
                        occupied_streets[source].push(max_route_id)
                        average_counter[source] += 1
                        max_counter[source] = max(max_counter[source], 1)
                            
    return (occupied_streets, Routes, max_counter,
            average_counter, used_walk_indx, num_avail_source)


def particle_simulation_fixed_source(graph,
                                     num_new_routes,
                                     feasible_walks,
                                     feasible_walks_source,
                                     birth_type):
    """
    At each iteration, we have particle_birth followed by particle_time_step
    """
    occupied_streets = {}
    Routes = {}
    num_feasible_walks = len(feasible_walks)
    num_avail_source = len(feasible_walks_source)
    Routes['max_id'] = 0
    used_walk_indx = -1
    max_counter = dict.fromkeys(graph.nodes(), 0)
    average_counter = dict.fromkeys(graph.nodes(), 0)
    while used_walk_indx < num_feasible_walks - 1:
        (occupied_streets,
         Routes,
         max_counter,
         average_counter,
         used_walk_indx,
         num_avail_source) = particle_birth_fixed_source(graph,
                                                       occupied_streets,
                                                       Routes,
                                                       max_counter,
                                                       average_counter,
                                                       num_new_routes,
                                                       feasible_walks,
                                                       feasible_walks_source,
                                                       used_walk_indx,
                                                       num_feasible_walks,
                                                       num_avail_source,
                                                       birth_type)
        (occupied_streets,
         Routes,
         max_counter,
         average_counter) = particle_time_step_fixed_source(graph,
                                                            occupied_streets,
                                                            Routes,
                                                            max_counter,
                                                            average_counter)

    return max_counter, average_counter

def rank_nonleafnodes(nonleaf_nodes, centrality_dict):

    val_node = sorted([(centrality_dict[node] , indx, node)
                      for indx, node in enumerate(nonleaf_nodes)],
                     reverse = True)
    indx_rank = [indx for _ , indx, __ in val_node]
    n = len(nonleaf_nodes)
    ranking = [0 for i in range(n)]
    for i in range(n):
        ranking[indx_rank[i]] = i + 1
    return ranking

    
def experiment1(graph):
    """
    Read the following from directory 'pre_data/p2p-Gnutella08/fixedsource'
        1. source files: sourceX_Y.txt
        2. walk files: shortWalksX_Y.txt
        3. install location files: installX_Y.txt
    
    Return:
        kendalltau and spearman for diff install_ratio and birth rate
    """
    if not graph.is_directed(): 
        raise ValueError("Graph must be DiGraph")
    nonleaf_nodes = get_nonleaf_nodes(graph)
    #data_dir = 'pre_data/example/fixedsource/'
    data_dir = 'pre_data/p2p-Gnutella08/fixedsource/'
    file_nos = []
    for myfile in os.listdir(data_dir):
        if myfile.endswith(".txt"):
            if myfile[:len('short')] == 'short':
                file_no = myfile[len('shortWalks'):-4]
                file_no = [int(i) for i in file_no.replace('_', ' ').split()]
                iratio, scenario = file_no
                file_nos.append((iratio, scenario))
            #print(os.path.join(data_dir, file))
    birth_rate = 1
    full_soc = 3
    birth_type = 'random_source'
    #birth_type = 'walk_at_random'
    for pair in file_nos:
        ratio, scene = pair
        walkfile = (data_dir + 'shortWalks' +
                    str(ratio) + '_' + str(scene) + '.txt')
        installfile = (data_dir + 'install' +
                    str(ratio) + '_' + str(scene) + '.txt')
        sourcefile = (data_dir + 'source' +
                    str(ratio) + '_' + str(scene) + '.txt')
        feasible_walks, feasible_walks_source = read_feasible_walks(walkfile)
        install_dict, install_nodes = get_install_dict(graph, installfile)
        source_nodes = get_source_nodes(graph, sourcefile)
        soc_btn = soc.fixed_source_betweenness_centrality(graph,
                                                          full_soc,
                                                          install_nodes,
                                                          source_nodes)
        standard_btn = standard_fixed_source.betweenness_centrality(
                     graph, source_nodes)
        #btn_ranking = node_values_to_ranking(soc_btn)
        num_new_routes = int(math.ceil(birth_rate* len(source_nodes)))
        max_counter, average_counter = particle_simulation_fixed_source(
                                     graph,
                                     num_new_routes,
                                     feasible_walks,
                                     feasible_walks_source,
                                     birth_type)
        #sim_ranking = node_values_to_ranking(average_counter)
        #sim_ranking2 = node_values_to_ranking(max_counter)
        #ken_soc, spr_soc = compute_stats(sim_ranking, btn_ranking)
        #ken_soc2, spr_soc2 = compute_stats(sim_ranking2, btn_ranking)
        #print ratio, scene, ken_soc.correlation,\
        #      spr_soc.correlation
        sim = rank_nonleafnodes(nonleaf_nodes, average_counter)
        btnrank = rank_nonleafnodes(nonleaf_nodes, standard_btn)
        myrank = rank_nonleafnodes(nonleaf_nodes, soc_btn)
        ken_soc, spr_soc = compute_stats(sim, myrank)
        ken_std, spr_std = compute_stats(sim, btnrank)
        print 'myrank', ratio, scene, ken_soc.correlation, spr_soc.correlation
        print 'std', ratio, scene, ken_std.correlation, spr_std.correlation

    #ken_file = open('kendall.txt', 'w')
    #spr_file = open('spearman.txt', 'w')



def node_values_to_ranking(node_values):
    # node_values is dict
    n = len(node_values)
    val_node = sorted([(node_values[node] , node) for node in node_values],
                     reverse = True)
    node_rank = [node for _, node in val_node]
    ranking = [0 for i in range(n)]
    for i in range(n):
        ranking[node_rank[i]] = i + 1
    return ranking
        
def compute_stats(rank1, rank2):
    return sc.kendalltau(rank1, rank2), sc.spearmanr(rank1, rank2)
    

def get_nonleaf_nodes(graph):
    """ Returns nodes with out_degree > 0. """
    return [node for node in graph.nodes() if graph.out_degree(node) > 0]

def get_source_from_st_pair(stfile):
    source = np.genfromtxt(stfile, dtype = 'int')[:,0]
    return source.tolist()

def experiment2(graph):
    """ Random Feasible Walks.
    Read the following from directory 'pre_data/p2p-Gnutella08/fixedsource'
        1. source files: sourceX_Y.txt
        2. walk files: shortWalksX_Y.txt
        3. install location files: installX_Y.txt
    
    Return:
            congestionX_Y_Z.txt
            X -- install_ratio
            Y -- scenario
            Z -- birth_rate * 100
    """
    if not graph.is_directed(): 
        raise ValueError("Graph must be DiGraph")
    nonleaf_nodes = get_nonleaf_nodes(graph)
    data_dir = 'pre_data/example/randomwalks/'
    #data_dir = 'pre_data/p2p-Gnutella08/randomwalks/'
    outdir = 'post_data/example/randomwalks/'
    file_nos = []
    for myfile in os.listdir(data_dir):
        if myfile.endswith(".txt"):
            if myfile[:len('randomWalks')] == 'randomWalks':
                file_no = myfile[len('randomWalks'):-4]
                file_no = [int(i) for i in file_no.replace('_', ' ').split()]
                iratio, scenario = file_no
                file_nos.append((iratio, scenario))
    birth_rate = 0.5
    full_soc = 3
    birth_type = 'random_source'
    #birth_type = 'walk_at_random'
    for pair in file_nos:
        ratio, scene = pair
        filetag = str(ratio) + '_' + str(scene) + '.txt'
        filetag_birth = str(ratio) + '_' + str(scene) + '_'\
                        + str(int(birth_rate*100)) + '.txt'
        walkfile = (data_dir + 'randomWalks' + filetag)
        installfile = (data_dir + 'install' + filetag)
        sourcefile = (data_dir + 'source_target' + filetag)
        feasible_walks, feasible_walks_source = read_feasible_walks(walkfile)
        install_dict, install_nodes = get_install_dict(graph, installfile)
        source_nodes = get_source_from_st_pair(sourcefile)
        num_new_routes = int(math.ceil(birth_rate* len(source_nodes)))
        max_counter, average_counter = particle_simulation_fixed_source(
                                     graph,
                                     num_new_routes,
                                     feasible_walks,
                                     feasible_walks_source,
                                     birth_type)
        myfile = open(outdir + 'congetion' + filetag_birth, 'w' )
        for node in sorted(graph.nodes()):
            myfile.write(str(average_counter[node]) + '\n')
        myfile.close()
        



if __name__ == '__main__':
    graph = nx.davis_southern_women_graph()
    graph = nx.DiGraph(graph)
    #graphfile = '../../data/p2p-Gnutella08.txt'
    #graph = nx.read_edgelist(graphfile, nodetype=int, create_using=nx.DiGraph())
    graph = max(nx.weakly_connected_component_subgraphs(graph), key=len)
    graph = nx.convert_node_labels_to_integers(graph, first_label=0)
    #experiment1(graph)
    experiment2(graph)
