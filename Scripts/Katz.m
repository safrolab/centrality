function [katz_cent] = Katz(A, p)
A(A>0) = 1;
[n, ~] = size(A);
a1 = 0.95*1/abs(eigs(A,1));
a1 = min(a1, p);
%a1 = 1/abs(eigs(A,1)) - 0.01;
init_cen = ones(n,1);
I = speye(n);
W1  = (I- a1*A)\init_cen;
W1 = W1/norm(W1);
katz_cent = W1;
end