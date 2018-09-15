import networkx as nx


if __name__ == '__main__':
    graph =  nx.read_edgelist('../../data/minesota_graph.txt', nodetype = int)
    conn = sorted(nx.connected_components(graph), key = len, reverse=True)
    centrality = nx.current_flow_betweenness_centrality(graph)
    myfile = open('minnesota_current_flow_centrality.txt', 'w')
    for node in sorted(centrality):
        myfile.write(str(centrality[node]) + '\n')
    myfile.close()
    
    
