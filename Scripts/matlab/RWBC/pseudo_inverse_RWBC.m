function [total_centrality] = pseudo_inverse_RWBC(A);
[~,n]  = size(A);

D = A*ones(n,1);
D = spdiags([D], 0, n, n);
L = D - A;

L_plus = pinv(L);

total_centrality = zeros(n,1);
for s=1:n
    for t= 1:n
        if s ~= t
            s_index = zeros(n,1);
            s_index(s) = 1;
            s_index(t) = -1;
            V = s'*Lplus;
            D_V = spdiags([V], 0, n,n);
            flow_mat = D_V*A;
            %G = digraph(flow_mat);
            %plot(G,'EdgeLabel',G.Edges.Weight)
            net_flow_mat = abs(flow_mat - flow_mat');
            centrality = 0.5*net_flow_mat*ones(n,1);
            %centrality = (s_index*TA)';
            centrality(s) = 1;
            centrality(t) = 1;
            total_centrality = total_centrality + centrality;
        end
    end
end