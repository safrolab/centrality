%ssget('Newman/karate')
%load('Newman/karate.mat')
load('two_clique_Newman.mat')
%ssget('HB/lap_25')%
%load('HB/lap_25')
%load('HB/saylr1')
%load('grid10x10.mat')
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

%source = 17;
%terminal = 11;
steps= 3;
num_labelled_nodes = 11;
labelled_nodes = randperm(n,num_labelled_nodes);
%labelled_nodes = [6 7 5];
I = speye(n);
J = sparse(n,n);

D = A*ones(n,1);
for i=1:num_labelled_nodes
   indx = labelled_nodes(i);
   J (indx, indx) = 1;
end
%%

B = sparse(n*steps, n*steps);
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

%Add self-loops
Ink = speye(n*steps,n*steps);
B = Ink +B;
X = sparse(n*steps, n);
Y = sparse(n*steps, n);
for i=0:steps-1
    X(i*n+1:(i+1)*n, :) = I;
end
Y(1:n,:) = I;

D_B = B*ones(n*steps,1);
D_B = spdiags(D_B, 0, n*steps, n*steps);
D_B_inv = D_B.^(-1);
D_B_inv(D_B_inv > 1) = 0;
D_B_inv = spdiags(D_B_inv, 0, n*steps, n*steps);
M_B = D_B_inv*B;
U = (Ink - M_B)^(-1);
L_B = D_B - B;
L_B_t = L_B;
L_B_t(n*(steps -1) + 1: n*steps, :) = [];
L_B_t(:,n*(steps -1) + 1: n*steps) = [];

%%
%remove soc terminal nodes
%M_B_t = M_B;
%M_B_t (n*(steps -1) + 1: n*steps, :) = [];
%M_B_t (:,n*(steps -1) + 1: n*steps) = [];
btn_cen = zeros(n,1);
for source=1:n
    for terminal=1:n
        if source < terminal
            L_B_t = L_B;
            L_B_t(n*(steps -1) + 1: n*steps, :) = [];
            L_B_t(:,n*(steps -1) + 1: n*steps) = [];
            term_nodes = [terminal];
            for i=1:steps-2
                term_nodes(i + 1) = terminal + i*n;
            end
            %isolated nodes

            L_B_t(term_nodes, :) = [];
            L_B_t(:, term_nodes) = [];
            [~, n_L_B] = size(L_B_t);
            s = zeros(n_L_B, 1);
            if source < terminal
                s(source) = 1;
            else
                s(source-1) = 1;
            end
            V_t = L_B_t\s;
            V = sparse(n*steps,1);
            for i= 1:n*(steps-1)
                j = mapping(i, terminal, n);
                if j >0
                    V(i) = V_t(j);
                else
                    V(i) = 0;
                end
            end
            st_cen_B = zeros(n*steps,1);
            for node=1:n*steps
                st_cen_B(node) = net_in_flow(V, node,B);
            end
            st_cen_A = get_flow_vec(st_cen_B, n, steps);

            btn_cen = btn_cen + st_cen_A;
        end
    end
end
btn_cen = btn_cen/((n-2)*(n-1));
btn_cen