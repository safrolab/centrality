function[latest_carriers, num_new_carriers, latest_infected, ...
    num_new_suspt, local_active, global_active, is_recovered] = ...
    carrier_spread_time_step(G,local_active,global_active, new_carriers,...
    num_new_carriers, p,n, is_susceptible, is_recovered, ...
    latest_infected, num_new_suspt)
latest_carriers = zeros(n,1);
indx_carrier = 1; 
indx_suspt = num_new_suspt + 1;
for i=1:num_new_carriers
    node = new_carriers(i);
    neigh = successors(G, node);
    for j=1:G.outdegree(node)
        u = neigh(j);
        if is_recovered(u) == 0
            if local_active(u) == 0
                new_status = binornd(1,p);
                local_active(u) = new_status;
                if new_status == 1
                    global_active(u) = 1;
                    if is_susceptible(u) == 1
                        is_recovered(u) = 1;
                        latest_infected(indx_suspt) = u;
                        indx_suspt = indx_suspt + 1;
                    elseif is_susceptible(u) == 0
                        latest_carriers(indx_carrier) = u;
                        indx_carrier = indx_carrier + 1;
                    end
               end
           end
       end
   end
   
end
num_new_carriers = indx_carrier - 1;
num_new_suspt = indx_suspt - 1;

end