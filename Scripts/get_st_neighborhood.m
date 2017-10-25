function [nodes, new_s, new_t, new_B] = get_st_neighborhood(Z, B,s,t,n, steps)

term_nodes = sparse(steps,1);

term_nodes(1) = t;
for i=1:steps-1
    term_nodes(i + 1) = t + i*n;
end
s_index = Z(s,:); 

if any(s_index(term_nodes) > 0) == 1
    term_vec = sparse(n*steps + 1, 1);
    term_vec(term_nodes) = 1;
    term_vec(n*steps + 1) = 1;
    t_index = (Z*term_vec);

    intersect = s_index' & t_index;
    temp = 1:n*steps + 1;
    nodes_  = temp(intersect);
    nodes = [ nodes_ n*steps + 1];
    new_s = find(nodes == s, 1);
    new_t = find(nodes == n*steps + 1, 1, 'last');
    new_B = B(nodes,nodes);
else
    nodes = -1;
    new_s = -1;
    new_t = -1;
    new_B = [];
    
end
end