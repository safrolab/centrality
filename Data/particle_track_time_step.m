function[current_soc, current_node, visited] = ...
    particle_track_time_step(G, current_soc, full_soc, current_node, ...
    visited, immunize_dic,install_dic)
%{
Updates a time step in the particle track model:
    A particle chooses a neighbor uniformly at random and moves 
    to it. 
    If the next neighbor is immunied it stops
    If it runs out of soc, it stops
    If out degree is 0, it stops
%}
if current_soc > 0
    if G.outdegree(current_node) > 0
        neigh = successors(G, current_node);
        next_node = randsample(neigh,1);
        if immunize_dic(next_node) == 0
            if install_dic(next_node) == 0
                current_soc = current_soc - 1;
                visited(next_node) = 1;
            elseif install_dic(next_node) ==1
                current_soc = full_soc;
                visited(next_node) = 1;
            end
        elseif immunize_dic(next_node) == 1
            next_node = -1;
        end
    elseif G.outdegree(current_node) == 0
        next_node = -1;
    end
elseif current_soc == 0
    next_node = -1;
end
current_node = next_node;
end
