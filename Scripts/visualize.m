load('Newman/karate')
A = Problem.A;
[~, n] = size(A);
k = 2;
x = 20;
I = speye(n);
J = speye(n);
for i=x:n
    J(i,i) =0;
end
B = zeros(n*k, n*k);
B = sparse(B);
for i=0:k-1
    B(i*n+1:(i+1)*n,1:n) = J*A;
end
for i=0:k-2
    B(i*n+1:(i+1)*n,(i+1)*n +1:(i+2)*n) = (I-J)*A;
end
spy(B^100)
[V, D, W] = eigs(B)