%ssget('Newman/karate')
%load('Newman/karate.mat')
%ssget('HB/lap_25')%
%load('HB/lap_25')
%load('HB/saylr1')
load('grid10x10.mat')
%load('twitter.mat')
%load('star_path_star2.mat')
%load('HB/1138_bus')
%A = Problem.A;
%G = graph(A);
%A = G.adjacency;
%plot(G)
A(A > 0) = 1;
[~, n] = size(A);

%% parameters


I = speye(n);
D = A*ones(n,1);
D = diag(D);
L = sparse(D - A);
source = 1;
target = 10;

btn_cen = zeros(n,1);
for source=1:n
    for terminal=1:n
        if source ~= terminal
            L_t = L;
            L_t(terminal,:) = [];
            L_t(:,terminal) = [];      
            s = zeros(n-1, 1);
            if source < terminal
                s(source) = 1;
            else
                s(source-1) = 1;
            end
            V_t = L_t\s;
            V = sparse(n,1);
            V(1:terminal-1) = V_t(1:terminal-1);
            V(terminal) = 0;
            if terminal +n < n
                V(terminal+1:n) = V_t(terminal:n-1);
            end
            D_V = spdiags([V], 0, n,n);
            flow_mat = D_V*A;
            %G = digraph(flow_mat);
            %plot(G,'EdgeLabel',G.Edges.Weight)
            net_flow_mat = abs(flow_mat - flow_mat');
            centrality = 0.5*net_flow_mat*ones(n,1);
            centrality(source) = 1;
            centrality(terminal) = 1;
            btn_cen = btn_cen + centrality;
        end
    end
end
U = [centrality(1:10) centrality(11:20) ...
    centrality(21:30) centrality(31:40)...
    centrality(41:50) centrality(51:60)...
    centrality(61:70) centrality(71:80)... 
    centrality(81:90) centrality(91:100)];
heatmap(U);
