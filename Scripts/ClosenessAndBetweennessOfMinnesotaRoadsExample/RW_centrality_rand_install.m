function[centrality] = RW_centrality_rand_install(A, steps, n_install)

A(A > 0) = 1;
[~, n] = size(A);
num_labelled_nodes = n_install;
labelled_nodes = randperm(n,num_labelled_nodes);
I = speye(n);
J = sparse(n,n);

D = A*ones(n,1);
for i=1:num_labelled_nodes
   indx = labelled_nodes(i);
   J (indx, indx) = 1;
end


B = sparse(n*steps + 1, n*steps + 1);
for i=0:steps-1
    B(i*n+1:(i+1)*n,1:n) = A*J;
end
B(1:n,1:n) = A*J;
for i=0:steps-2
    B(i*n+1:(i+1)*n,(i+1)*n +1:(i+2)*n) = A*(I-J);
end
B(1:n,n+1:2*n) = A*(I-J);

centrality_B = zeros(n*steps + 1,1);
I_z = speye(n*steps + 1, n*steps + 1);

Z = I_z;
B_n = I_z;
%for i=1:n + 1
%     B_n = B_n*B;
%    Z = Z + B_n;
%end
alpha = 0.7*abs(1/eigs(A,1));
Z = (I_z -alpha*B)\I_z;
X = sparse(n*steps + 1, n);
for i=0:steps-1
    X(i*n+1:(i+1)*n, :) = I;
end
for source = 1:n
    source
    for terminal= 1:n
        if source ~= terminal
            term_nodes = sparse(steps,1);
            term_nodes(1) = terminal;
            for i=1:steps-1
                term_nodes(i + 1) = terminal + i*n;
            end
            copy_B = B;
            for i=1:steps
                copy_B(term_nodes(i), :) =sparse(1,n*steps  +1);
            end
            
            %term_nodes connect to t (n*steps + 1)
            copy_B(term_nodes, n*steps + 1) =1;
            [nodes, new_s, new_t, new_B] = get_st_neighborhood(Z, copy_B,source,terminal,n, steps);
            if new_s > 0
                [~, new_n] = size(new_B);
                [cen] = st_biased_random_walk_BC(new_B, new_n, new_s, new_t);
                centrality_B(nodes) = centrality_B(nodes) + cen;
           end
        end
   end
end

c_end   = centrality_B(end);
centrality_B = centrality_B/c_end;
centrality = centrality_B'*X;

end
