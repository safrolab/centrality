"""
Compute stats on simulation Vs centrality

"""
import networkx as nx
import random
import math
import scipy.stats as sc
import sys
import os
import numpy as np


def get_nonleaf_nodes(graph):
    """ Returns nodes with out_degree > 0. """
    return [node for node in graph.nodes() if graph.out_degree(node) > 0]

def  get_centrality_from_file(graph, centrality_file):
    myfile = open(centrality_file, 'r')
    centrality = {}
    node = 0
    for line in myfile:
        centrality[node] = float(line)
        node += 1
    return centrality


def rank_nonleafnodes(nonleaf_nodes, centrality_dict):
    '''
    val_node = sorted([(centrality_dict[node] , indx, node)
                      for indx, node in enumerate(nonleaf_nodes)],
                     reverse = True)
    indx_rank = [indx for _ , indx, __ in val_node]
    n = len(nonleaf_nodes)
    ranking = [0 for i in range(n)]
    for i in range(n):
        ranking[indx_rank[i]] = i + 1
    '''
    val_node = [centrality_dict[node] for node in nonleaf_nodes]
    ranking = sc.rankdata(val_node, method = 'min')
    return ranking

def compute_stats(rank1, rank2):
    return sc.kendalltau(rank1, rank2), sc.spearmanr(rank1, rank2)
    
    
def scale_centrality(centrality):
    max_val = max([centrality[node] for node in centrality])
    scale = 1.0/max_val
    for node in centrality:
        centrality[node] *= scale
    return centrality


def randomwalk_stats_birth(graph):
    data_dir = 'post_data/example/randomwalks/'
    file_nos_birth = {}
    nonleafnodes = get_nonleaf_nodes(graph)
    for myfile in os.listdir(data_dir):
        if myfile.endswith(".txt"):
            if myfile[:len('congetion')] == 'congetion':
                file_no = myfile[len('congetion'):-4]
                file_no = [int(i) for i in file_no.replace('_', ' ').split()]
                iratio, scenario, birth = file_no
                if (iratio, scenario) in file_nos_birth:
                    file_nos_birth[(iratio, scenario)].append(birth)
                else:
                    file_nos_birth[(iratio, scenario)] = [birth]
    
    for iratio, scenario in file_nos_birth:
        filetag = str(iratio) + '_' + str(scenario)
        RWBCfile = data_dir + 'RWBC' + filetag + '.txt'
        RWBC_dict = get_centrality_from_file(graph, RWBCfile)
        RWBC_dict = scale_centrality(RWBC_dict)
        RWBC_rank = rank_nonleafnodes(nonleafnodes, RWBC_dict)
        for birth in file_nos_birth[(iratio, scenario)]:
            congetionfile = data_dir + 'congetion' + filetag \
                          + '_' + str(birth) + '.txt'
            congetion_dict = get_centrality_from_file(graph, congetionfile)
            congetion_dict = scale_centrality(congetion_dict)
            congetion_rank = rank_nonleafnodes(nonleafnodes, congetion_dict)
            kendall, spearman = compute_stats(RWBC_rank, congetion_rank)
            print kendall.correlation, spearman.correlation
            #for node in graph.nodes():
            #    print node, RWBC_dict[node], congetion_dict[node]

def randomwalk_stats(graph, graphname):

    data_dir = 'post_data/' + graphname + '/randomwalks/'
    file_nos= []
    nonleafnodes = get_nonleaf_nodes(graph)
    for myfile in os.listdir(data_dir):
        if myfile.endswith(".txt"):
            if myfile[:len('counter')] == 'counter':
                file_no = myfile[len('counter'):-4]
                file_no = [int(i) for i in file_no.replace('_', ' ').split()]
                iratio, scenario = file_no
                file_nos.append(file_no)
    
    for iratio, scenario in file_nos:
        filetag = str(iratio) + '_' + str(scenario)
        RWBCfile = data_dir + 'RWBC' + filetag + '.txt'
        RWBC_dict = get_centrality_from_file(graph, RWBCfile)
        RWBC_dict = scale_centrality(RWBC_dict)
        congetionfile = data_dir + 'counter' + filetag + '.txt'
        congetion_dict = get_centrality_from_file(graph, congetionfile)
        congetion_dict = scale_centrality(congetion_dict)
        RWBC_rank = rank_nonleafnodes(nonleafnodes, RWBC_dict)
        congetion_rank = rank_nonleafnodes(nonleafnodes, congetion_dict)
        kendall, spearman = compute_stats(RWBC_rank, congetion_rank)
        print kendall.correlation, spearman.correlation
        #for i in range(len(nonleafnodes)):
        #    node = nonleafnodes[i]
        #s    print node, RWBC_rank[i], congetion_rank[i], '\t \t', RWBC_dict[node], congetion_dict[node]

                

if __name__ == '__main__':
    #graph = nx.davis_southern_women_graph()
    #graph = nx.DiGraph(graph)
    #graphfile = '../../data/p2p-Gnutella08.txt'
    graphfile = 'p2p-Gnutella08.txt'
    graphname = 'p2p-Gnutella08'
    print graphname
    graph = nx.read_edgelist(graphfile, nodetype=int, create_using=nx.DiGraph())
    #graph = max(nx.weakly_connected_component_subgraphs(graph), key = len)
    #graph = nx.convert_node_labels_to_integers(graph, first_label = 0, ordering='sorted')
    randomwalk_stats(graph, graphname)
