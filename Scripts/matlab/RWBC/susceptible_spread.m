function [total_active,total_recovered ] = ...
    susceptible_spread(G, start_node, full_soc, p, is_susceptible)
%{
Get list of current infected nodes
apply susceptible_spread_single_source to each infected node
get new infected list
Repeat

%}
n = G.numnodes;
is_recovered = zeros(n,1);
global_active = zeros(n,1);
is_recovered(start_node) = 1;
global_active(start_node) = 1;
num_current_source = 1;
current_infected = [start_node];
%step = 1;
while num_current_source > 0
    %if step == 3
    %    break
    %end
    %step = step + 1;
    next_source_nodes = zeros(n,1);
    num_next_source = 0;
    for i=1:num_current_source
        current_node = current_infected(i);
        [latest_infected, num_new_suspt, global_active, is_recovered] = ...
    susceptible_spread_single_source(G,current_node, full_soc,...
        is_susceptible, is_recovered, global_active, p, n);
        [next_source_nodes, num_next_source] = ...
            update_new_recovered(next_source_nodes,num_next_source,...
            latest_infected, num_new_suspt);
        
    end
    num_current_source = num_next_source;
    current_infected = next_source_nodes;
end

total_active = nnz(global_active);
total_recovered = nnz(is_recovered);
%a = find(global_active)'
%b = find(is_recovered)
%[find(global_active) find(is_recovered)]
end