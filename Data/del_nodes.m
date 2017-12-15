%{
Preprocess graph
Get largest WCC
%}
clear
%g = 'collabo';
g = 'collabo2';
%g= 'wiki';
%g = 'gnutella';
if strcmp(g, 'collabo')
    load('ca-HepTh.mat')
    A = Problem.A;
    G = graph(A);
    n = G.numnodes;
    conn = conncomp(G);
    to_remove = zeros(n,1);
    for node = 1:n
        if conn(node) ~= 1
            to_remove(node) = node;
        end
    end
    to_remove = to_remove(to_remove>0);
    G = rmnode(G,to_remove);
    A = G.adjacency;
    G = digraph(A);
elseif strcmp(g, 'wiki')
    load('wiki-Vote.mat')
    A = Problem.A;
    G = digraph(A);
    n = G.numnodes;
    to_remove = zeros(n,1);
    for node = 1:n
        if G.indegree(node) == 0 && G.outdegree(node) == 0 
            to_remove(node) = node;
        end
    end
    to_remove = to_remove(to_remove>0);
    G = rmnode(G,to_remove);
    A = G.adjacency;
    G = digraph(A);
elseif strcmp(g, 'gnutella')
    load('p2p-Gnutella04.mat')
    A = Problem.A;
    G = digraph(A);
    n = G.numnodes;
    to_remove = zeros(n,1);
    for node = 1:n
        if G.indegree(node) == 0 && G.outdegree(node) == 0 
            to_remove(node) = node;
        end
    end
    to_remove = to_remove(to_remove>0);
    G = rmnode(G,to_remove);
    A = G.adjacency;
    G = digraph(A);
elseif strcmp(g, 'collabo2')
    load('ca-GrQc.mat')
    A = Problem.A;
    G = graph(A);
    n = G.numnodes;
    conn = conncomp(G);
    to_remove = zeros(n,1);
    for node = 1:n
        if conn(node) ~= 3
            to_remove(node) = node;
        end
    end
    to_remove = to_remove(to_remove>0);
    G = rmnode(G,to_remove);
    A = G.adjacency;
    G = digraph(A);
end