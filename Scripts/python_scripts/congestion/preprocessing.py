"""Preprocessing for soc experiments.

This script generates random feasible walks and writes them to file. The walks
are used in the soc experiments.

Output:
    graphname/shortWalks1_1.txt  # contains random shortest feasible walks
    graphname/install1_1.txt  # contains WCU install locations
    installX_Y.txt  # X = install_ratio, Y = Yth scenario
"""
import networkx as nx
import random
import math
import scipy.stats as sc
import sys
import congetion


def install_nodes2file(graphname, install_nodes, install_ratio, scenario_no):
    """Write install_nodes to file. """
    install_no = str(int(install_ratio*100))
    outfile = 'pre_data/' + graphname \
              + '/install' + install_no \
              + '_' + str(scenario_no) + '.txt'
    myfile = open(outfile, 'w')
    out = "".join([str(node)+'\n' for node in install_nodes])
    myfile.write(out)
    myfile.close() 


def install_nodes2file_source(graphname, install_nodes,
                              install_ratio, scenario_no, walktype):
    """Write install_nodes to file. """
    install_no = str(int(install_ratio*100))
    if walktype == 'shortest':
        outfile = 'pre_data/' + graphname \
                  + '/fixedsource/install' + install_no \
                  + '_' + str(scenario_no) + '.txt'
    elif walktype == 'random' or walktype == 'random_path':
        outfile = 'pre_data/' + graphname \
                  + '/randomwalks/install' + install_no \
                  + '_' + str(scenario_no) + '.txt'
    else:
        raise ValueError('walktype should be random or shortest')
    myfile = open(outfile, 'w')
    out = "".join([str(node)+'\n' for node in install_nodes])
    myfile.write(out)
    myfile.close() 


def source_nodes2file(graphname, source_nodes, install_ratio, scenario_no):
    """Write install_nodes to file. """
    install_no = str(int(install_ratio*100))
    outfile = 'pre_data/' + graphname \
              + '/fixedsource/source' + install_no \
              + '_' + str(scenario_no) + '.txt'
    myfile = open(outfile, 'w')
    out = "".join([str(node)+'\n' for node in source_nodes])
    myfile.write(out)
    myfile.close() 

  
def append_walk2file(walkfile, walk):
    """append feasible walk to file. """
    myfile = open(walkfile, 'a')
    out = " ".join([str(node) for node in walk])
    out += '\n'
    myfile.write(out)
    myfile.close()


def write_files_fixed_source(graph, graphname, walktype):
    """
    Output:
        graphname/fixedsource/shortWalks1_1.txt
        graphname/fixedsource/install1_1.txt  # contains WCU install locations
        graphname/fixedsource/source1_1.txt # contains source nodes
    """
    full_soc = 3
    num_walks = 20000
    num_scenarios = 1
    num_source = 10  # number of source nodes for each scenario
    I_Ratios = [0.01, 0.05, 0.1, 0.2, 0.4, 0.8]
    #I_Ratios = [0.2]
    candidate_source_nodes = nonleaf_nodes(graph)
    for install_ratio in I_Ratios:
        print install_ratio
        num_install = int(math.ceil(install_ratio*nx.number_of_nodes(graph)))
        for scenario_no in range(num_scenarios):
            install_no = str(int(install_ratio*100))
            walkfile_adr = 'pre_data/' + graphname \
                           + '/fixedsource/shortWalks' + install_no \
                           + '_' + str(scenario_no) + '.txt'
            walkfile = open(walkfile_adr, 'w')
            install_nodes = random.sample(graph.nodes(), num_install)
            source_nodes = random.sample(candidate_source_nodes, num_source)
            install_dict = dict.fromkeys(graph.nodes(), False)
            for node in install_nodes:
                install_dict[node] = True
            install_nodes2file_source(graphname,
                                      install_nodes,
                                      install_ratio,
                                      scenario_no,
                                      walktype)
            source_nodes2file(graphname,
                              source_nodes,
                              install_ratio,
                              scenario_no)
            soc_graph = congetion.construct_soc_graph(graph,
                                                      full_soc,
                                                      install_dict)
            soc_graph_reverse = soc_graph.reverse()
            for _ in range(num_walks):
                s = random.choice(source_nodes)
                t = random.choice(graph.nodes())
                if s != t:
                    walk = congetion.get_random_feasible_walk(soc_graph,
                                                              soc_graph_reverse,
                                                              full_soc,
                                                              s, t,
                                                              'shortest')
                    if len(walk) > 0:
                        append_walk2file(walkfile_adr, walk)

def valid_walk(graph, walk):
  """For Debugging: Check if all edges in walk exist in graph. 
  Note: The walk 1 -> 2 -> 3 is given as walk = [3, 2, 1]
  """
  for i, k in enumerate(walk[:-1]):
    if not graph.has_edge(walk[i + 1], walk[i]):
      return False
  return True

def write_s_t_random_walks(graph, graphname, walktype):
    """
    Output:
        graphname/randomwalks/randomWalks1_1.txt
        graphname/randomwalks/install1_1.txt  # contains WCU install locations
        graphname/randomwalks/source_target1_1.txt # contains source nodes
    """
    full_soc = 4
    num_walks = 200  # number random walks per (s, t) pair
    num_scenarios = 1
    num_st_pairs = 1  # number of (s, t) pairs for each scenario
    #I_Ratios = [0.01, 0.05, 0.1, 0.2, 0.4, 0.8]
    I_Ratios = [0.1]
    candidate_source_nodes = nonleaf_nodes(graph)
    used_pairs = {}
    for install_ratio in I_Ratios:
        print install_ratio
        num_install = int(math.ceil(install_ratio*nx.number_of_nodes(graph)))
        for scenario_no in range(num_scenarios):
            install_no = str(int(install_ratio*100))
            walkfile_adr = 'pre_data/' + graphname \
                           + '/randomwalks/randomWalks' + install_no \
                           + '_' + str(scenario_no) + '.txt'
            walkfile = open(walkfile_adr, 'w')
            install_nodes = random.sample(graph.nodes(), num_install)
            #install_nodes = [5, 11, 23, 6, 9, 4, 12]
            print 'install_nodes:', install_nodes
            install_dict = dict.fromkeys(graph.nodes(), False)
            for node in install_nodes:
                install_dict[node] = True
            install_nodes2file_source(graphname,
                                      install_nodes,
                                      install_ratio,
                                      scenario_no,
                                      walktype)
            soc_graph = congetion.construct_soc_graph(graph,
                                                      full_soc,
                                                      install_dict)
            soc_graph_reverse = soc_graph.reverse()
            for _ in range(num_st_pairs):
                s = random.choice(candidate_source_nodes)
                t = random.choice(graph.nodes())
                #s = 26
                #t = 24
                print s,t
                if s != t:
                    if (s, t) not in used_pairs:
                        soc_s = (full_soc - 1, s)
                        if nx.has_path(soc_graph, soc_s, t):  #  feasible walk exists
                            used_pairs[(s,t)] = 1
                            for _ran_walk in range(num_walks):
                                walk = congetion.get_random_feasible_walk(
                                     soc_graph,
                                     soc_graph_reverse,
                                     full_soc,
                                     s, t,
                                     walktype)
                                if not valid_walk(graph, walk):
                                  print 'walk not valid'
                                append_walk2file(walkfile_adr, walk)
                        else:
                            print 'no feasible path', s, t
            st_pairs2file(graphname, used_pairs, install_ratio, scenario_no)


def st_pairs2file(graphname, used_pairs, install_ratio, scenario_no):
    """Write install_nodes to file. """
    install_no = str(int(install_ratio*100))
    outfile = 'pre_data/' + graphname \
              + '/randomwalks/source_target' + install_no \
              + '_' + str(scenario_no) + '.txt'
    myfile = open(outfile, 'w')
    out = "".join([str(s) + ' ' + str(t) +'\n' for s, t in used_pairs])
    myfile.write(out)
    myfile.close() 




'''
def write_files(graph, graphname):
    """
    Output:
        graphname/shortWalks1_1.txt  # contains random shortest feasible walks
        graphname/install1_1.txt  # contains WCU install locations
        
    """

    full_soc = 3
    num_walks = 200
    num_scenarios = 10
    #I_Ratios = [0.01, 0.02, 0.05, 0.1, 0.2, 0.4, 0.8]
    I_Ratios = [0.2]
    for install_ratio in I_Ratios:
        num_install = int(install_ratio*nx.number_of_nodes(graph))
        for scenario_no in range(num_scenarios):
            install_no = str(int(install_ratio*100))
            walkfile_adr = 'pre_data/' + graphname \
                            + '/shortWalks' + install_no \
                            + '_' + str(scenario_no) +'.txt'
            walkfile = open(walkfile_adr, 'w')
            install_nodes = random.sample(graph.nodes(), num_install)
            install_dict = dict.fromkeys(graph.nodes(), False)
            for node in install_nodes:
                install_dict[node] = True
            install_nodes2file(graphname,
                               install_nodes,
                               install_ratio,
                               scenario_no)
            soc_graph = congetion.construct_soc_graph(graph,
                                                      full_soc,
                                                      install_dict)
            for _ in range(num_walks):
                s = random.choice(graph.nodes())
                t = random.choice(graph.nodes())
                
                walk = congetion.get_random_feasible_walk(soc_graph,
                                                          full_soc,
                                                          s, t,
                                                          'shortest')
                if len(walk) > 0:
                    #direct = nx.shortest_path_length(graph, s, t)
                    #walk.append(direct)
                    append_walk2file(walkfile_adr, walk)
'''                   
def nonleaf_nodes(graph):
    """ Returns nodes with out_degree > 0. """
    return [node for node in graph.nodes() if graph.out_degree(node) > 0]

      
if __name__ == '__main__':
    #graph = nx.davis_southern_women_graph()
    #graph = nx.DiGraph(graph)
    #graphfile = '../../data/p2p-Gnutella08.txt'
    graphfile = 'p2p-Gnutella08.txt'
    graphname = 'p2p-Gnutella08'
    #graphname = 'example'
    walktype = 'random'
    #walktype = 'random_path'
    print graphname
    graph = nx.read_edgelist(graphfile, nodetype=int, create_using=nx.DiGraph())
    #graph = max(nx.weakly_connected_component_subgraphs(graph), key=len)
    #graph = nx.convert_node_labels_to_integers(graph, first_label=0, ordering='sorted')
    #myfile = open(graphname + '.txt', 'w')
    #for u, v in sorted(graph.edges()):
    #  myfile.write(str(u) + ' ' + str(v) +  '\n')
    #myfile.close()
    #write_files(graph, graphname)
    #write_files_fixed_source(graph, graphname, walktype)
    write_s_t_random_walks(graph, graphname, walktype)

     
    
