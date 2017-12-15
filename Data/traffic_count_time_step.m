function[current_soc, current_node, visit_count] = ...
    traffic_count_time_step(G, current_soc, full_soc, current_node, ...
    visit_count,install_dic)
%{
Updates a time step in the particle track model:
    A particle chooses a neighbor uniformly at random and moves 
    to it. 
    If it runs out of soc, it stops
    If out degree is 0, it stops
%}
if current_soc > 0
    if G.outdegree(current_node) > 0
        neigh = successors(G, current_node);
        next_node = randsample(neigh,1);
        if install_dic(next_node) == 0
            current_soc = current_soc - 1;
            visit_count(next_node) = visit_count(next_node) + 1;
        elseif install_dic(next_node) ==1
            current_soc = full_soc;
            visit_count(next_node) = visit_count(next_node) +1;
        end
    elseif G.outdegree(current_node) == 0
        next_node = -1;
    end
elseif current_soc == 0
    next_node = -1;
end
current_node = next_node;
end
