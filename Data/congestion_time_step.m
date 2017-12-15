function[soc, new_occupied, counter, occupied_dic, num_particles] = ...
    congestion_time_step(G, soc, full_soc, new_occupied, counter, occupied_dic, ...
    num_particles, install_dic)
%{
Updates a time step in the congestion model:
    A particle choose an unoccupied neighbor uniformly at random and moves 
    to it. If all neighors are occupied, then the particle rests
    soc: soc(i) gives the current soc of the particle at node i
    new_occupied: A list of newly occupied nodes
    counter: counter(i) is the number of times node i is occupied
    occupied_dic: occupied_dic(i) = 1 if node i is occupied, 0 otherwise
    occ_size: Number of particles in system
%}
latest_occupied = zeros(num_particles, 1);
indx = 1;
for i=1:num_particles
   node = new_occupied(i);
   if soc(node) > 0
       if G.outdegree(node) > 0
           neigh = successors(G, node);
           free_neigh = neigh(occupied_dic(neigh) ~= 1);
           [num_free, ~] = size(free_neigh);
           if num_free > 0
               next_node = randsample(free_neigh,1);
               counter(next_node) = counter(next_node) + 1;
               occupied_dic(next_node) = 1;
               occupied_dic(node) = 0;
               latest_occupied(indx) = next_node;
               indx = indx + 1;
               if install_dic(next_node) == 1 % next_node is charging unit
                   soc(next_node) = full_soc;
               else
                   soc(next_node) = soc(node) -1;
                   soc(node) = 0;
               end
           elseif num_free == 0 % particle rests, soc reduces
               counter(node) = counter(node) + 1;
               soc(node) = soc(node) - 1;
               latest_occupied(indx) = node;
               indx = indx + 1;
           end
       elseif  G.outdegree(node) == 0
           counter(node) = counter(node) + 1;
           soc(node) = soc(node) - 1;
           latest_occupied(indx) = node;
           indx = indx + 1;
       end
   elseif soc(node) == 0 % particle dies out
       occupied_dic(node) = 0; 
       num_particles = num_particles - 1;
   end
end
new_occupied = latest_occupied;
end