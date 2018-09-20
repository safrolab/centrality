function [flow] = net_in_flow(V, node,B)

in_column = B(:, node);
if all(in_column(:) == 0)
    flow = 0;
else  
in_neigh = find(in_column);
[num_neigh, ~] = size(in_neigh);
flow = 0;

for i=1:num_neigh
    neigh = in_neigh(i);
    flow = flow + abs(V(node) - V(neigh));
end
end


end
