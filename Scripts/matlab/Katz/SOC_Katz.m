function [soc_katz] = SOC_Katz(A, steps, install_percentage)
A(A > 0) = 1;
[~, n] = size(A);
num_labelled_nodes = ceil(install_percentage*n);
labelled_nodes = randperm(n,num_labelled_nodes);
I = speye(n);
J = sparse(n,n);
D = A*ones(n,1);
for i=1:num_labelled_nodes
   indx = labelled_nodes(i);
   J (indx, indx) = 1;
end
B = sparse(n*steps, n*steps);
for i=0:steps-1
    B(i*n+1:(i+1)*n,1:n) = A*J;
end
B(1:n,1:n) = A*J;
for i=0:steps-2
    B(i*n+1:(i+1)*n,(i+1)*n +1:(i+2)*n) = A*(I-J);
end
B(1:n,n+1:2*n) = A*(I-J);
Ink = speye(n*steps,n*steps);
X = sparse(n*steps, n);
Y = sparse(n*steps, n);
for i=0:steps-1
    X(i*n+1:(i+1)*n, :) = I;
end
Y(1:n,:) = I;
%a1 = 1/abs(eigs(A,1)) - 0.01;
%a2 = 1/abs(eigs(B,1)) - 0.01;
a1 = 0.8*1/abs(eigs(A,1));
%a1 = 0.8*1/4.4470;
a2 = 0.99*1/abs(eigs(B,1));
a2 = max(a1,a2);
%a2 = 0.8;
init_cen = ones(n,1);
for i=1:num_labelled_nodes
   indx = labelled_nodes(i);
   init_cen(indx) = 1;
end
%W1  = (I- a1*A)\init_cen;
W2 = Y'*((speye(n*steps) - a2*B)\(X*ones(n,1)));
%W1 = W1/norm(W1);
W2 = W2/norm(W2);
soc_katz = W2;
end