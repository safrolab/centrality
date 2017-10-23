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
steps= 3;
num_labelled_nodes = 20;
labelled_nodes = randperm(n,num_labelled_nodes);
%labelled_nodes = [1 34];
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
    B(i*n+1:(i+1)*n,1:n) = (I-J)*A*J;
end
B(1:n,1:n) = A*J;
for i=0:steps-2
    B(i*n+1:(i+1)*n,(i+1)*n +1:(i+2)*n) = (I-J)*A*(I-J);
end
B(1:n,n+1:2*n) = A*(I-J);

Ink = speye(n*steps,n*steps);
X = sparse(n*steps, n);
Y = sparse(n*steps, n);
for i=0:steps-1
    X(i*n+1:(i+1)*n, :) = I;
end
Y(1:n,:) = I;
%%
%a1 = 1/abs(eigs(A,1)) - 0.01;
%a2 = 1/abs(eigs(B,1)) - 0.01;
a1 = 0.95*1/abs(eigs(A,1));
%a2 = 0.95*1/abs(eigs(B,1));
%%
W2 = Y'*((speye(n*steps) - a1*B)\X);
spy(W2)
neighborhood = W2;
neighborhood(neighborhood > 0) = 1;
spy(neighborhood)
iD = diag(neighborhood(:,1));
iD(~any(iD,2), :) = [];
%%
