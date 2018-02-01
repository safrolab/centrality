function [nodes, new_s, new_t, new_B] = get_st_neighborhood(Z, ...
    B, s, t, n, steps)
%{
Return subgraph of B such that every node is at a finite distance to t

new_B -- submatrix of B 
new_s -- new label of s as submatrix is relabelled
new_t -- new label of t as submatrix is relabelled
%}

term_nodes = zeros(steps,1);  % soc nodes corresponding to t
term_nodes(1) = t;
for i=1:steps-1
    term_nodes(i + 1) = t + i*n;
end
s_index = Z(s,:);  % reachable nodes from s
if any(s_index(term_nodes) > 0) == 1  %  if t reachable from s
    term_vec = sparse(n*steps + 1, 1);  % determine reachable nodes from t
    term_vec(term_nodes) = 1;
    term_vec(n*steps + 1) = 1;
    t_index = (Z*term_vec);  % reachable nodes from t
    intersect = s_index' & t_index;  % node reachable from s and t or not
    temp = 1:n*steps + 1;
    nodes_  = temp(intersect); 
    nodes = [nodes_ n*steps + 1];  % append node 'n*steps + 1'
    new_s = find(nodes == s, 1);  % new indx in submatrix
    new_t = find(nodes == n*steps + 1, 1, 'last');
    new_B = B(nodes,nodes);  % submatrix of B
else
    nodes = -1;
    new_s = -1;
    new_t = -1;
    new_B = [];
    
end
end