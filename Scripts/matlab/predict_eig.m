load('Newman/karate')
%ssget('HB/lap_25')%
%load('HB/lap_25')
%load('HB/saylr1')
%load('grid20x20.mat')
%load('HB/1138_bus')
A = Problem.A;
G = graph(A);
A = G.adjacency;

[~, n] = size(A);



I = speye(n);
%A = A - I; %remove loops
J = sparse(zeros(n));

D = A*ones(n,1);
for i = 1:5
    J(i,i) = 1; 
end
%steps= 4;
max_step= 30;
out = zeros(max_step-1,5);
for steps=2:max_step

    B = zeros(n*steps, n*steps);
    B = sparse(B);
    for i=0:steps-1
        %B(i*n+1:(i+1)*n,1:n) = (I-J)*A*J;
        B(i*n+1:(i+1)*n,1:n) = (I-J)*J;
    end
    %B(1:n,1:n) = A*J;
    B(1:n,1:n) = J;
    for i=0:steps-2
        %B(i*n+1:(i+1)*n,(i+1)*n +1:(i+2)*n) = (I-J)*A*(I-J);
        B(i*n+1:(i+1)*n,(i+1)*n +1:(i+2)*n) = (I-J)*(I-J);
    end
    %B(1:n,n+1:2*n) = A*(I-J);
    B(1:n,n+1:2*n) = (I-J);
    out(steps-1,1) = eigs(B,1);
    out(steps-1,2) = steps;
    out(steps-1, 3) = eigs(A*J,1);
    out(steps-1, 4) = eigs(A*(I-J),1);
    out(steps-1, 5) = eigs(A,1);
end
out
plot(out(:,1))
