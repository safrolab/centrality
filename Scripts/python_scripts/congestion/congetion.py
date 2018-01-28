import networkx as nx
import random
import math
import scipy.stats as sc
import sys
sys.path.insert(0, '/home/hushiji/Research/centrality/Scripts/python_scripts/')
import betweenness as soc


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
      

def construct_soc_graph(graph, full_soc, install_dict):
    """ Given graph, return soc_graph"""
    if not graph.is_directed():  # convert to digraph
        graph = nx.DiGraph(graph)
    soc_graph = nx.DiGraph()
    for node in graph.nodes():  # add nodes to soc_graph
        if install_dict[node]:
            soc_node = (full_soc-1, node)
            soc_graph.add_node(soc_node)
        else:
            for i in range(full_soc):
                soc_node = (i, node)
                soc_graph.add_node(soc_node)
    for u, v in graph.edges():  # add edges to soc_graph
        if install_dict[u] and install_dict[v]:
            soc_u = (full_soc - 1,  u)
            soc_v = (full_soc - 1, v)
            soc_graph.add_edge(soc_u, soc_v)
        elif install_dict[u]:
            soc_u = (full_soc - 1, u)
            soc_v = (full_soc - 2, v)
            soc_graph.add_edge(soc_u, soc_v)
        elif install_dict[v]:
            soc_v = (full_soc - 1, v)
            for i in range(full_soc):
                soc_u = (i, u)
                soc_graph.add_edge(soc_u, soc_v)
        else:
            for i in range(1, full_soc):
                soc_u = (i, u)
                soc_v = (i-1, v)
                soc_graph.add_edge(soc_u, soc_v)
    for node in graph.nodes():  # add endpoint nodes and edges to soc_graph
        if install_dict[node]:
            soc_node = (full_soc - 1, node)
            soc_graph.add_edge(soc_node, node)
        else:
            for i in range(full_soc):
                soc_node = (i, node)
                soc_graph.add_edge(soc_node, node)
    return soc_graph


def get_random_feasible_walk(soc_graph, full_soc, s, t, walk_type):
    soc_s = (full_soc -1, s)
    if nx.has_path(soc_graph, soc_s, t):
        if walk_type == 'shortest':
            paths = [p for p in \
            nx.all_shortest_paths(soc_graph,source=soc_s,target=t)]
            soc_path = random.choice(paths)
            walk = [node for _, node in soc_path[:-1]]
            walk.reverse()

    else:
        #print 'no feasible path'
        walk = []
    return walk


def particle_time_step(graph, occupied_streets, Routes, max_counter):
    """
    Perform a time step of particle simulation.
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
                if max_counter[next_step] < node_congestion:
                    max_counter[next_step] = node_congestion
            else:
                occupied_streets[next_step] = Queue()
                occupied_streets[next_step].push(route_id)
        if route_queue.len() == 0:
            del occupied_streets[street]
            
            
    return occupied_streets, Routes, max_counter
    
          
def particle_birth(soc_graph, graph,occupied_streets, Routes, max_counter,
                   birth_rate, full_soc):
    # add birth_rate*num_nodes routes
    # choose birth_rate*num_nodes
    num_new_routes = int(math.ceil(birth_rate*nx.number_of_nodes(graph)))
    origin = random.sample(graph.nodes(), num_new_routes)
    target = random.sample(graph.nodes(), num_new_routes)   
    max_route_id = Routes['max_id'] 
    for s, t in zip(origin, target):
        walk = get_random_feasible_walk(soc_graph, full_soc, s, t, 'shortest')
        if len(walk) > 0:
            max_route_id += 1
            Routes['max_id'] = max_route_id
            Routes[max_route_id] = walk
            if s in occupied_streets:
                occupied_streets[s].push(max_route_id)
                node_congestion = occupied_streets[s].len()
                if max_counter[s] < node_congestion:
                    max_counter[s] = node_congestion
            else:
                occupied_streets[s] = Queue()
                occupied_streets[s].push(max_route_id)
    return occupied_streets, Routes, max_counter


def particle_simulation(soc_graph, graph, birth_rate, full_soc, niter):
    """
    At each iteration, we have particle_birth followed by particle_time_step
    """
    occupied_streets = {}
    Routes = {}
    Routes['max_id'] = 0
    max_counter = dict.fromkeys(graph.nodes(), 0)
    
    for _ in range(niter):
        occupied_streets, Routes, max_counter = particle_birth(
                                              soc_graph, graph,
                                              occupied_streets, 
                                              Routes, max_counter, birth_rate,
                                              full_soc)
        occupied_streets, Routes, max_counter = particle_time_step(
                                              graph, occupied_streets, Routes,
                                              max_counter)

    return max_counter


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
    
def experiment(graph):
    """
    Data collection for soc paper
    Input: 
        1. graph

    
    Parameters to vary:
        1. full_soc
        2. install_ratio  #  we use random installations
        3. birth_rate
        4. niter  #  number iterations for congestion simulation
    
    Return:
        kendalltau and spearman for diff install_ratio and birth rate
    """
    #ken_file = open('kendall.txt', 'w')
    #spr_file = open('spearman.txt', 'w')
    full_soc = 3
    niter = 20000
    niter_install = 10
    #I_Ratios = [0.01, 0.02, 0.05, 0.1, 0.2, 0.4, 0.8, 1]
    #B_Rates = [0.1, 0.2, 0.4, 0.8, 1]
    I_Ratios = [0.2]
    B_Rates = [0.01]
    btn = nx.betweenness_centrality(graph)
    btn_ranking = node_values_to_ranking(btn)
    for install_ratio in I_Ratios:
        num_install = int(install_ratio*nx.number_of_nodes(graph))
        for _ in range(niter_install):
            install_nodes = random.sample(graph.nodes(), num_install)
            install_dict = {}
            for node in graph.nodes():
                install_dict[node] = False
            for node in install_nodes:
                install_dict[node] = True
            soc_graph = construct_soc_graph(graph, full_soc, install_dict)
            soc_btn = soc.betweenness_centrality(graph, full_soc, install_nodes)
            soc_ranking = node_values_to_ranking(soc_btn)
            for birth_rate in B_Rates:
                max_counter = particle_simulation(
                            soc_graph, graph, birth_rate,full_soc, niter)
                sim_ranking = node_values_to_ranking(max_counter)
                ken_strd, spr_strd = compute_stats(sim_ranking, btn_ranking)
                ken_soc, spr_soc = compute_stats(sim_ranking, soc_ranking)
                ken_str = " ".join([str(install_ratio), str(birth_rate), 
                                   str(ken_strd.correlation), 
                                   str(ken_soc.correlation), 
                                   str(ken_strd.pvalue),
                                   str(ken_soc.correlation), ' \n']) 
                spr_str = " ".join([str(install_ratio), str(birth_rate), 
                                   str(spr_strd.correlation), 
                                   str(spr_soc.correlation), 
                                   str(spr_strd.pvalue),
                                   str(spr_soc.pvalue), ' \n']) 
                #ken_file.write(ken_str)
                #spr_file.write(spr_str)
                #print install_ratio, birth_rate, ken_strd.correlation, \
                #      ken_soc.correlation
                #print install_ratio, birth_rate, spr_strd.correlation, \
                #      spr_soc.correlation
                print ken_strd.correlation, ken_soc.correlation
                print spr_strd.correlation, spr_soc.correlation
                #print ken_strd.pvalue, ken_soc.pvalue
                #print spr_strd.pvalue, spr_soc.pvalue
   
def debug():
    #graph = nx.karate_club_graph()
    graph = nx.davis_southern_women_graph()
    graph = nx.convert_node_labels_to_integers(graph, first_label=0)
    full_soc = 2
    num_install = 5
    birth_rate = 1
    niter = 20000
    #s = 0
    #t = 20
    install_nodes = random.sample(graph.nodes(), num_install)
    install_dict = {}
    for node in graph.nodes():
        install_dict[node] = False
    for node in install_nodes:
        install_dict[node] = True
    soc_graph = construct_soc_graph(graph, full_soc, install_dict)
    max_counter = particle_simulation(soc_graph, graph, birth_rate,full_soc,
                                      niter)
    btn = nx.betweenness_centrality(graph, endpoints=True)
    soc_btn = soc.betweenness_centrality(graph, full_soc, install_nodes)
    sim_ranking = node_values_to_ranking(max_counter)
    btn_ranking = node_values_to_ranking(btn)
    soc_ranking = node_values_to_ranking(soc_btn)
    ken_strd, spr_strd = compute_stats(sim_ranking, btn_ranking)
    ken_soc, spr_soc = compute_stats(sim_ranking, soc_ranking)
    print ken_strd.correlation, ken_soc.correlation
    print spr_strd.correlation, spr_soc.correlation
    print ken_strd.pvalue, ken_soc.pvalue
    print spr_strd.pvalue, spr_soc.pvalue
    sort_congestion = sorted([(max_counter[node],node) for node in graph.nodes()])
    #for i, node in sort_congestion:
    #    print(i, node, btn[node])
    #walk = get_random_feasible_walk(soc_graph, full_soc, s, t, 'shortest')
    #print walk, install_nodes
         
if __name__ == '__main__':
    graph = nx.davis_southern_women_graph()
    #graphfile = '/home/hushiji/Research/centrality/Scripts/data/minnesota.mtx'
    #graph = nx.read_edgelist(graphfile, nodetype=int)
    graph = nx.convert_node_labels_to_integers(graph, first_label=0)
    experiment(graph)
