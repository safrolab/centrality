%ssget('Newman/karate')
%load('Newman/karate.mat')
%ssget('HB/lap_25')%
%load('HB/lap_25')
%load('HB/saylr1')
%load('grid10x10.mat')
load('two_clique_Newman.mat')
%load('two_clique_Hayato.mat')
%load('two_clique_Hayato2.mat')
%load('two_clique_Hayato3.mat')
%load('two_clique_Hayato5.mat')
%load('twitter.mat')
%load('star_path_star2.mat')
%load('HB/1138_bus')
%A = Problem.A;
G = graph(A);
%A = G.adjacency;
%plot(G)
A(A > 0) = 1;
[~, n] = size(A);

%% parameters


steps= 3;
num_labelled_nodes = n;
labelled_nodes = randperm(n,num_labelled_nodes);
%labelled_nodes = [21 41 61 81 92 94 96 98 ];
I = speye(n);
J = sparse(n,n);

D = A*ones(n,1);
for i=1:num_labelled_nodes
   indx = labelled_nodes(i);
   J (indx, indx) = 1;
end
%%

B = sparse(n*steps + 1, n*steps + 1);
%B = sparse(B);
for i=0:steps-1
    %B(i*n+1:(i+1)*n,1:n) = (I-J)*A*J;
    B(i*n+1:(i+1)*n,1:n) = A*J;
end
B(1:n,1:n) = A*J;
for i=0:steps-2
    %B(i*n+1:(i+1)*n,(i+1)*n +1:(i+2)*n) = (I-J)*A*(I-J);
    B(i*n+1:(i+1)*n,(i+1)*n +1:(i+2)*n) = A*(I-J);
end
B(1:n,n+1:2*n) = A*(I-J);

%add terminal soc level to t1 (n*steps + 1) <- not necessary
%{
D1 = A*ones(n,1) - A*J*ones(n,1);
D1(D1 >0) = 1;
B(n*(steps-1)+1:n*steps, n*steps +1) = D1;

%add edge t1 -> t3
B(n*steps +1, n*steps +3) = 1;
%add edge t2 -> t3
B(n*steps +2, n*steps +3) = 1;
%}

%term_nodes = [terminal];




centrality_B = zeros(n*steps + 1,1);
I_z = speye(n*steps + 1, n*steps + 1);

Z = I_z;
for i=1:n + 1
    Z = Z + B^i;
end
%%
X = sparse(n*steps + 1, n);
for i=0:steps-1
    X(i*n+1:(i+1)*n, :) = I;
end
parfor source = 1:n
    for terminal= 1:n
        if source ~= terminal
            %source = 60;
            %terminal  = 94;
            %[source, terminal]
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
                parTemp = zeros(n*steps + 1,1);
                parTemp(nodes) = cen;
                centrality_B = centrality_B + parTemp;
                

           end
        end
   end
end


%%
c_end   = centrality_B(end);
centrality_B = centrality_B/c_end;
%%

centrality = centrality_B'*X;
%%
centrality = centrality';
%%
%{
V = [centrality(1:10) centrality(11:20) ...
   centrality(21:30) centrality(31:40)...
    centrality(41:50) centrality(51:60)...
    centrality(61:70) centrality(71:80)... 
   centrality(81:90) centrality(91:100)];
heatmap(V);
%}
%heatmap(nod_net_flow )
%L1 = Incidence_mat*Incidence_mat';
%A1 = copy_B + copy_B';
%A1(A1 >0) = 1;
%L2 =sparse(diag(A1*ones(n*steps+3,1))) - A1;
%{
U = [nod_net_flow(1:10) nod_net_flow(11:20) ...
    nod_net_flow(21:30) nod_net_flow(31:40)...
    nod_net_flow(41:50) nod_net_flow(51:60)...
    nod_net_flow(61:70) nod_net_flow(71:80)... 
    nod_net_flow(81:90) nod_net_flow(91:100)];
%heatmap(U)clf
V = [centrality(1:10) centrality(11:20) ...
    centrality(21:30) centrality(31:40)...
    centrality(41:50) centrality(51:60)...
    centrality(61:70) centrality(71:80)... 
    centrality(81:90) centrality(91:100)];
%heatmap(U)clf
heatmap(V);
%}

%%
