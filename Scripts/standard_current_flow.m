%ssget('Newman/karate')
load('Newman/karate.mat')
%ssget('HB/lap_25')%
%load('HB/lap_25')
%load('HB/saylr1')
%load('grid10x10.mat')
%load('twitter.mat')
%load('star_path_star2.mat')
%load('HB/1138_bus')
A = Problem.A;
G = graph(A);
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
        if source < terminal
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
            V = sparse(n*steps,1);
            V(1:terminal-1) = V_t(1:terminal-1);
            V(terminal) = 0;
            if terminal +n < n
                V(terminal+1:n) = V_t(terminal:n-1);
            end

        end
    end
end
V