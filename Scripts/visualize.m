%ssget('Newman/karate')
%load('Newman/karate')
%ssget('HB/lap_25')%
%load('HB/lap_25')
%load('HB/saylr1')
%load('grid10x10.mat')
load('star_path_star2.mat')
%load('HB/1138_bus')
%A = Problem.A;
G = graph(A);
A = G.adjacency;
%plot(G)



[~, n] = size(A);

steps= 3;
num_labelled_nodes = 1;
labelled_nodes = zeros(num_labelled_nodes,1);
labelled_nodes(1) = 7;
I = speye(n);
%A = A - I; %remove loops
J = sparse(zeros(n));

D = A*ones(n,1);
for i=1:num_labelled_nodes
   indx = labelled_nodes(i);
   J(indx, indx) = 1;
end


B = zeros(n*steps, n*steps);
B = sparse(B);
for i=0:steps-1
    B(i*n+1:(i+1)*n,1:n) = (I-J)*A*J;
end
B(1:n,1:n) = A*J;
for i=0:steps-2
    B(i*n+1:(i+1)*n,(i+1)*n +1:(i+2)*n) = (I-J)*A*(I-J);
end
B(1:n,n+1:2*n) = A*(I-J);

Ink = speye(n*steps,n*steps);
X = sparse(zeros(n*steps, n));
Y = sparse(zeros(n*steps, n));
for i=0:steps-1
    X(i*n+1:(i+1)*n, :) = I;
end
Y(1:n,:) = I;

a1 = 1/abs(eigs(A,1)) - 0.01;
a2 = 1/abs(eigs(B,1)) - 0.01;

init_cen = ones(n,1);
for i=1:num_labelled_nodes
   indx = labelled_nodes(i);
   init_cen(indx) = 2;
end
W1  = (I- a1*A)\init_cen;
W2 = Y'*((speye(n*steps) - a2*B)\(X*ones(n,1)));
%W1 = W1/norm(W1);
%W2 = W2/norm(W2);
%U = [W1';W2'];
%[newW1, sort_order] = sort(W1);
%newW2 = W2(sort_order,:);

%plot([1:n]', newW1,'LineWidth',3)
%hold on
%scatter([1:n]', newW2, 'filled')
%hold off
scatter(W1, W2)
W1 = W1/norm(W1);
W2 = W2/norm(W2);
[katz, katz_order] = sort(W1,'descend');
[Bound_katz, Bound_katz_order] = sort(W2,'descend');
[[1:n]', katz_order, Bound_katz_order]
[[1:n]', W1,W2]