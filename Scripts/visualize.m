%ssget('Newman/karate')
%load('Newman/karate')
%ssget('HB/lap_25')%
%load('HB/lap_25')
%load('HB/saylr1')
load('grid10x10.mat')
%load('HB/1138_bus')
%A = Problem.A;
G = graph(A);
A = G.adjacency;
%plot(G)



[~, n] = size(A);

steps= 4;

I = speye(n);
%A = A - I; %remove loops
J = sparse(zeros(n));

D = A*ones(n,1);

for i = 1:10
    v = randi(n)
    J(v,v) = 1; 
    %J(sort_order(i),sort_order(i)) = 1;   
end


%J(1,1) = 1;
%J(2,2) =1;
%J(6,6)= 1;
%J(3,3) = 1;
%J(11,11) = 1;
%J(15,15)= 1;
%J(23,23)= 1;
%J(24,24) = 1;
%J(20,20) = 1;
%J(25,25) = 1;
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
%Z = Y'*B^u*X;
%spy(Z - A^u)
%spy(B)
%spy(Z)
%clearvars
a1 = 1/eigs(A,1) - 0.01;
%a1 = 0.1;
a2 = 1/eigs(B,1) - 0.01;
W1  = (I- a1*A)^(-1)*ones(n,1);
W2 = Y'*(speye(n*steps) - a2*B)^(-1)*X*ones(n,1);
colormap('jet');
W1 = W1/norm(W1);
W2 = W2/norm(W2);
U = [W1';W2'];
[newW1, sort_order] = sort(W1);
newW2 = W2(sort_order,:);

plot([1:n]', newW1,'LineWidth',3)
hold on
scatter([1:n]', newW2, 'filled')
hold off
%bar([W1,W2])
%bar([newW1,newW2])

%imagesc(U');
%colorbar;
%C = Y'*(B^10001 +B^10001 + B^10002+ B^10003+B^10004)*X;
%spy(C)
%clear;