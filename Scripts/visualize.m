load('Newman/karate')
A = Problem.A;
[~, n] = size(A);
steps= 5;
x = 1; %number of nodes with charging unit
a = 0.1;
I = speye(n);
J = speye(n);
for i=x+1:n
    J(i,i) =0;
end
B = zeros(n*steps, n*steps);
B = sparse(B);
for i=0:k-1
    B(i*n+1:(i+1)*n,1:n) = (I-J)*A*J;
end
B(1:n,1:n) = A*J;
for i=0:steps-2
    B(i*n+1:(i+1)*n,(i+1)*n +1:(i+2)*n) = (I-J)*A*(I-J);
end
B(1:n,n+1:2*n) = A*(I-J);
spy(B^20)
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
u = 4;
Z = Y'*B^u*X;
Z1= Y'*B^u'*X;
Z2 = Z + Z1';
spy(Z - A^u)
clc