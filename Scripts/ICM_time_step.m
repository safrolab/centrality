function[latest_active_nodes, active_nodes, num] = ICM_time_step(G,active_nodes,newly_active, new_size, p,n)
latest_active_nodes = zeros(n,1);
indx = 1; 
for i=1:new_size
   node = newly_active(i);
   neigh = G.neighbors(node);
   for j=1:G.degree(node)
       u = neigh(j);
       if active_nodes(u) == 0
           new_status = binornd(1,p);
           active_nodes(u) = new_status;
           if new_status == 1
               latest_active_nodes(indx) = u;
               indx = indx + 1;
           end
       end
   end
   
end
num = indx -1;
end