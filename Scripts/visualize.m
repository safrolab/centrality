%load('Newman/karate')
%ssget('HB/saylr1')
load('HB/lap_25')
%load('HB/saylr1')

A = Problem.A;

[~, n] = size(A);
steps= 3;
x = 0; %number of nodes with charging unit

I = speye(n);
A = A - I; %remove loops
J = speye(n);
for i=x+1:n
    J(i,i) =0;
end
J(1,1) = 1;
J(2,2) =1;
J(6,6)= 1;
J(3,3) = 1;
J(11,11) = 1;
J(15,15)= 1;
J(23,23)= 1;
J(24,24) = 1;
J(20,20) = 1;
J(25,25) = 1;
%for i=x+1:n
%    J(i,i) =0;
%end
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
%spy(B^10)
%colormap('default')
%imagesc(B^100)
%colorbar
Ink = speye(n*steps,n*steps);
X = sparse(zeros(n*steps, n));
Y = sparse(zeros(n*steps, n));
for i=0:steps-1
    X(i*n+1:(i+1)*n, :) = I;
    %Y(i*n+1:(i+1)*n, :) = I;
end
Y(1:n,:) = I;
%spy(X'*B*X-A)
u =33 ;
Z = Y'*B^u*X;
%spy(Z - A^u)
spy(B)
%spy(Z)
Z(1,1);
%clearvars
a = 0.14;
clc
W1  = (I- a*A)^(-1)*ones(n,1);
W2 = Y'*(speye(n*steps) - a*B)^(-1)*X*ones(n,1)
imagesc(W2)
colormap('hot')
colorbar
