n = G1.numnodes;
conn = conncomp(G1);
to_remove = zeros(n,1);
for node = 1:n
if conn(node) ~= 1
to_remove(node) = node;
end
end
to_remove = to_remove(to_remove>0);
G1 = rmnode(G1,to_remove);