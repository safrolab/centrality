function[counter] = ...
    congestion(G, new_particles, full_soc, install, num_time_steps)

%%G is a directed graph
%function[soc, new_occupied, counter, occupied_dic, occ_size] = ...
 %   congestion_time_step(G, soc, full_soc, new_occupied, counter, occupied_dic, ...
 %   occ_size, install)

n = G.numnodes;
occupied_dic = zeros(n,1);
occupied_dic(new_particles) = 1;
counter = zeros(n,1);
counter(new_particles) = 1;
soc = zeros(n,1);
soc(new_particles) = full_soc;
[num_particles, ~] = size(new_particles);
install_dic = zeros(n,1);
install_dic(install) = 1;
for i = 1:num_time_steps
    [soc, new_particles, counter, occupied_dic, num_particles] = ...
        congestion_time_step(G, soc, full_soc, new_particles, counter, ...
        occupied_dic, num_particles, install_dic);
    if num_particles ==0
        break
    end
end
end