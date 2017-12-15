%{
Post=process data
%}
G1 = rmnode(G, top_soc_k);
G2 = rmnode(G, top_kaz);
G3 = rmnode(G, top_deg);
A1 = G1.adjacency;
G1_ = graph(A1);
A2 = G2.adjacency;
G2_ = graph(A2);
A3 = G3.adjacency;
G3_ = graph(A3);
g1map = node_mapping_rmnode(G.numnodes, top_soc_k);
g2map = node_mapping_rmnode(G.numnodes, top_kaz);
g3map = node_mapping_rmnode(G.numnodes, top_deg);
%[soc_cover, katz_cover, deg_cover, top_kaz, top_soc_k, top_deg, install, test_nodes] = experiment_1(G,G.adjacency);
%fprintf('%.2f %.2f %.2f %5d %5d %5d %5d \n', soc_cover, katz_cover, deg_cover, ...
 %   G1.outdegree(g1map(test_nodes)), G2.outdegree(g2map(test_nodes)),...
%    G3.outdegree(g3map(test_nodes)), test_nodes)
[soc_cover, katz_cover, deg_cover, ...
    G1.outdegree(g1map(test_nodes)), G2.outdegree(g2map(test_nodes)),...
    G3.outdegree(g3map(test_nodes))];
