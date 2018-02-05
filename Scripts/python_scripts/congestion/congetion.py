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



def walk2path(walk):
  """Returns a path. Removes cycles
  Note: for path 1 -> 2 -> 3, walk = [3, 2, 1]
  """
  i = 1
  s = walk[-i]
  idx = walk.index(s)
  path = walk[:idx + 1]
  while idx > 0:
    i += 1
    temp = path[-i:]
    s = path[-i]
    idx = path.index(s)
    path = path[:idx ] + temp
  return path


def get_random_feasible_walk(soc_graph,
                             soc_graph_reverse,
                             full_soc,
                             s, t,
                             walk_type):
    soc_s = (full_soc -1, s)
    if nx.has_path(soc_graph, soc_s, t):
        if walk_type == 'shortest':
            paths = [p for p in \
            nx.all_shortest_paths(soc_graph,source=soc_s,target=t)]
            soc_path = random.choice(paths)
            walk = [node for _, node in soc_path[:-1]]
            walk.reverse()
        elif walk_type == 'random':
            walk = get_random_s_t_walk(soc_graph,
                                       soc_graph_reverse,
                                       full_soc,
                                       s, t)
            walk.reverse()
        elif walk_type == 'random_path':
            walk = get_random_s_t_walk_from_soc_path(soc_graph,
                                                     soc_graph_reverse,
                                                     full_soc,
                                                     s, t)
            walk.reverse()
            #walk = walk2path(walk)
        else:
            raise ValueError("walk_type must be 'shortest' or 'random'")
    else:
        #print 'no feasible path'
        walk = []
    return walk

def get_random_s_t_walk(soc_graph, soc_graph_reverse, full_soc, s, t):
    """ Return random feasible walk from s to t.
    """
    finite_dist = nx.shortest_path_length(soc_graph_reverse, t)
    soc_s = (full_soc -1, s)
    soc_walk = [soc_s]
    dist_to_target = finite_dist[soc_s]
    current_node = soc_s
    #dist = [finite_dist[soc_s]]
    visited = dict.fromkeys(soc_graph.nodes(), False)
    while dist_to_target > 1:
        neigh = []
        for node in soc_graph.neighbors(current_node):
            if node in finite_dist:
                neigh.append(node)
        current_node = random.choice(neigh)
        #dist.append(dist_to_target)
        soc_walk.append(current_node)
        dist_to_target = finite_dist[current_node]
    #print dist
    walk = [node for _, node in soc_walk]
    return walk

def get_random_s_t_walk_from_soc_path(soc_graph,
                                      soc_graph_reverse,
                                      full_soc,
                                      s, t):
    """ Return random feasible walk from s to t  from a random soc path.
    """
    finite_dist = nx.shortest_path_length(soc_graph_reverse, t)
    start_over = True
    while start_over == True:
        soc_s = (full_soc -1, s)
        current_node = soc_s
        soc_walk = [soc_s]
        visited = dict.fromkeys(soc_graph.nodes(), False)
        visited[current_node] = True
        soc, node = current_node
        for i in range(soc):
            visited[(i,node)] = True
        dist_to_target = finite_dist[soc_s]
        while dist_to_target > 1:
            neigh = []
            avail = 0
            for node in soc_graph.neighbors(current_node):
                if node in finite_dist and not visited[node]:
                    neigh.append(node)
                    avail += 1
            if avail > 0:
                current_node = random.choice(neigh)
                visited[current_node] = True
                soc, node = current_node
                for i in range(soc):
                    visited[(i,node)] = True
                soc_walk.append(current_node)
                dist_to_target = finite_dist[current_node]
                start_over = False
            else:  # dead end
                start_over = True
                break
    #print dist
    walk = [node for _, node in soc_walk]
    #print s, soc_walk
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
        walk = get_random_feasible_walk(soc_graph,
                                        soc_graph_reverse,
                                        full_soc,
                                        s, t,
                                        'shortest')
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


def debug2(graph):
    print 'number of nodes', nx.number_of_nodes(graph)
    full_soc = 3
    num_install = 4
    install_nodes = random.sample(graph.nodes(), num_install)
    #print 'install nodes', install_nodes
    install_dict = dict.fromkeys(graph.nodes(), False)
    for node in install_nodes:
        install_dict[node] = True
    soc_graph = construct_soc_graph(graph, full_soc, install_dict)
    soc_graph_reverse = soc_graph.reverse()
    s = random.choice(graph.nodes())
    t = random.choice(graph.nodes())
    soc_s = (full_soc -1, s)
    total_len = 0
    if nx.has_path(soc_graph, soc_s, t):
        for _ in range(1):
            walk = get_random_s_t_walk(soc_graph, soc_graph_reverse, full_soc, s, t)
            total_len += len(walk)
            #print s, t, 'graph distance:', nx.shortest_path_length(graph, s, t)
            #print 'random walk distance:', len(walk)
            print walk
        print 'average', total_len/1.0
        print 'actual', nx.shortest_path_length(graph, s, t)
    else:
        print "no feasible walk", s, t, nx.shortest_path_length(graph, s, t)

def debug3(graph):
    print '\t Debug function 3'
    full_soc = 3
    num_install = 4
    install_nodes = random.sample(graph.nodes(), num_install)
    #print 'install nodes', install_nodes
    install_dict = dict.fromkeys(graph.nodes(), False)
    for node in install_nodes:
        install_dict[node] = True
    soc_graph = construct_soc_graph(graph, full_soc, install_dict)

    for soc_node in soc_graph.nodes():
        if type(soc_node) == tuple:
            print 'node', soc_node
            print 'Graph neihborhood', graph.neighbors(soc_node[1])
            neigh = sorted([node for  node in soc_graph.neighbors(soc_node)])
            print 'soc graph neighborhood', neigh, '\n'
        else:
            neigh = [node for node in soc_graph.neighbors(soc_node)]
            print 'node', soc_node
            print 'Graph neihborhood', graph.neighbors(soc_node)
            print 'soc graph neighborhood', sorted(neigh), '\n'
    '''
    for node in graph.nodes():
        soc_node = (full_soc -3, node)
        print 'node', node
        if soc_node in soc_graph.nodes():
            print 'Graph neihborhood', graph.neighbors(node)
            neigh = sorted([neigh_node[1] for neigh_node in 
                            soc_graph.neighbors(soc_node) if type(neigh_node) == tuple])
            print 'soc graph neighborhood', neigh, neigh == sorted(graph.neighbors(node)),'\n'
    '''

def debug4():
    graph = nx.cycle_graph(10)
    full_soc = 3
    num_install = 4
    install_nodes = random.sample(graph.nodes(), num_install)
    install_dict = dict.fromkeys(graph.nodes(), False)
    for node in install_nodes:
        install_dict[node] = True
    soc_graph = construct_soc_graph(graph, full_soc, install_dict)

    for edge in soc_graph.edges():
        print edge


if __name__ == '__main__':
    graph = nx.davis_southern_women_graph()
    graph = nx.DiGraph(graph)
    #graphfile = '/home/hushiji/Research/centrality/Scripts/data/minnesota.mtx'
    #graph = nx.read_edgelist(graphfile, nodetype=int)
    graph = nx.convert_node_labels_to_integers(graph, first_label=0, ordering='sorted')
    #experiment(graph)
    debug3(graph)
