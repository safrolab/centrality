function[pos] = node_mapping_rmnode(num_nodes, to_remove)

allnodes = 1:num_nodes;
allnodes(to_remove) = 0;
new_nodes = allnodes(allnodes ~=0);
pos = zeros(num_nodes, 1);
[~, num_new] = size(new_nodes);
for i=1:num_new
    old = new_nodes(i);
    pos(old) = i;
end

end