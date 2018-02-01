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

    val_node = sorted([(centrality_dict[node] , indx, node)
                      for indx, node in enumerate(nonleaf_nodes)],
                     reverse = True)
    indx_rank = [indx for _ , indx, __ in val_node]
    n = len(nonleaf_nodes)
    ranking = [0 for i in range(n)]
    for i in range(n):
        ranking[indx_rank[i]] = i + 1
    return ranking

def compute_stats(rank1, rank2):
    return sc.kendalltau(rank1, rank2), sc.spearmanr(rank1, rank2)


def randomwalk_stats(graph):
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
        katfile = data_dir + 'katz' + filetag + '.txt'
        katz_dict = get_centrality_from_file(graph, katfile)
        katz_rank = rank_nonleafnodes(nonleafnodes, katz_dict)
        for birth in file_nos_birth[(iratio, scenario)]:
            congetionfile = data_dir + 'congetion' + filetag \
                          + '_' + str(birth) + '.txt'
            congetion_dict = get_centrality_from_file(graph, congetionfile)
            congetion_rank = rank_nonleafnodes(nonleafnodes, congetion_dict)
            kendall, spearman = compute_stats(katz_rank, congetion_rank)
            print kendall.correlation, spearman.correlation



if __name__ == '__main__':
    graph = nx.davis_southern_women_graph()
    graph = nx.DiGraph(graph)
    #graphfile = '../../data/p2p-Gnutella08.txt'
    #graph = nx.read_edgelist(graphfile, nodetype=int, create_using=nx.DiGraph())
    graph = max(nx.weakly_connected_component_subgraphs(graph), key = len)
    graph = nx.convert_node_labels_to_integers(graph, first_label = 0)
    randomwalk_stats(graph)
