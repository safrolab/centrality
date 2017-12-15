function[latest_active_nodes, soc,active_nodes, has_spread, num] = ...
    MT_time_step_2(G,soc, active_nodes,newly_active, has_spread, new_size, p,n)
latest_active_nodes = zeros(n,1);
indx = 1; 
for i=1:new_size
   node = newly_active(i);
   if has_spread(node) == 0
       node_soc = soc(node);
       neigh = successors(G, node);
       for j=1:G.outdegree(node)
           u = neigh(j);
           u_soc = soc(u);
           %if active_nodes(u) == 0
           if node_soc > u_soc + 1
               %prob = 1 - (1-p)^node_soc;
               if node_soc == 0
                   prob = 0;
               else
                    prob = p;
               end
               new_status = binornd(1,prob);
               active_nodes(u) = max(active_nodes(u), new_status);
               if new_status == 1
                   latest_active_nodes(indx) = u;
                   soc(u) = node_soc - 1;
                   indx = indx + 1;
               end
           elseif active_nodes(u) == 0
               prob = 1 - (1-p)^node_soc;
               new_status = binornd(1,prob);
               active_nodes(u) = max(active_nodes(u), new_status);
               if new_status == 1
                   latest_active_nodes(indx) = u;
                   soc(u) = max(u_soc,node_soc - 1);
                   indx = indx + 1;
               end
           end
       end
       has_spread(node) = 1;
   end
   

end
num = indx -1;
end