function[myrank] = node_rank(v, v_size)
rank = 1:v_size;
[~, node_perm] = sort(v, 'descend');
[~, myrank] = sort(node_perm);
end