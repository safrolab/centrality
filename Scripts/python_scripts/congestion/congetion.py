import networkx as nx
import random

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


def get_random_feasible_walk(soc_graph, s, t, walk_type):
    soc_s = (full_soc -1, s)
    if nx.has_path(soc_graph, soc_s, t):
        if walk_type == 'shortest':
            paths = [p for p in \
            nx.all_shortest_paths(soc_graph,source=soc_s,target=t)]
            soc_path = random.choice(paths)
            walk = [node for _, node in soc_path[:-1]]
    else:
        print 'no feasible path'
        walk = []
    return walk


def particle_time_step(graph, occupied_nodes, 
    """
    Perform a time step of particle simulation.
    At each step, a single particle in from each occupied node, moves to a 
    neighboring node.
    """
    
    for node in occupied_nodes:
        wait_list = occupied_nodes[node]
        next_path = wait_list.pop()
        move_to = next_path.pop()
        


def congestion_centrality(graph, full_soc, install_dict, walk_type):

    if walk_type == 'shortest':
        pass
    
    elif walk_type == 'random':
        pass 
    else:
        raise ValueError('walk_type must be "shortest" or "random"')

def time_step(graph,      
if __name__ == '__main__':

    graph = nx.karate_club_graph()
    full_soc = 3
    num_install = 5
    s = 0
    t = 20
    install_nodes = random.sample(graph.nodes(), num_install)
    install_dict = {}
    for node in graph.nodes():
        install_dict[node] = False
    for node in install_nodes:
        install_dict[node] = True
    soc_graph = construct_soc_graph(graph, full_soc, install_dict)
    walk = get_random_feasible_walk(soc_graph, s, t, 'shortest')
    print walk, install_nodes
    
    
