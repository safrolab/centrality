function [latest_infected, num_new_suspt, global_active, is_recovered] = ...
    susceptible_spread_single_source(G,current_node, full_soc,...
    is_susceptible, is_recovered, global_active, p, n)
%{
 Perform carrier_spread at most full_soc times
 current_node is a susceptible node
%}
    
is_recovered(current_node) = 1;
local_active = zeros(n. 1);
local_active(current_node) = 1;
new_carriers = [current_node];
num_new_carriers = 1;
num_new_suspt = 0;
for time_step=1:full_soc
    [new_carriers, num_new_carriers, latest_infected, num_new_suspt, ...
    local_active, global_active] = ...
    carrier_spread_time_step(G,local_active,global_active, new_carriers,...
    num_new_carriers, p,n, is_susceptible, is_recovered, num_new_suspt);
    if num_new_carriers == 0
        break
    end
end
end