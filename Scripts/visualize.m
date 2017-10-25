%ssget('Newman/karate')
%load('Newman/karate.mat')
%ssget('HB/lap_25')%
%load('HB/lap_25')
%load('HB/saylr1')
%load('grid10x10.mat')
load('twitter.mat')
%load('facebook2.mat')
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
num_labelled_nodes = ceil(0.1*n);
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
    %B(i*n+1:(i+1)*n,1:n) = (I-J)*A*J;
    B(i*n+1:(i+1)*n,1:n) = A*J;
end
B(1:n,1:n) = A*J;
for i=0:steps-2
    %B(i*n+1:(i+1)*n,(i+1)*n +1:(i+2)*n) = (I-J)*A*(I-J);
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
%%
%a1 = 1/abs(eigs(A,1)) - 0.01;
%a2 = 1/abs(eigs(B,1)) - 0.01;
a1 = 0.95*1/abs(eigs(A,1));
a2 = 0.95*1/abs(eigs(B,1));
a2 = max(a1,a2);
init_cen = ones(n,1);
for i=1:num_labelled_nodes
   indx = labelled_nodes(i);
   init_cen(indx) = 1;
end
W1  = (I- a1*A)\init_cen;
%%
W2 = Y'*((speye(n*steps) - a2*B)\(X*ones(n,1)));

%plot([1:n]', newW1,'LineWidth',3)
%hold on
%scatter([1:n]', newW2, 'filled')
%hold off

%%
W1 = W1/norm(W1);
W2 = W2/norm(W2);
%%
scatter(W1, W2,20, 'fill')
mdl = fitlm(W1,W2);
ylim=get(gca,'ylim');
xlim=get(gca,'xlim');
mystr = strcat('$\omega=', num2str(steps), ',m=', num2str(num_labelled_nodes));
mystr = strcat(mystr,',R^2=', num2str(round(mdl.Rsquared.Ordinary,2)), '$');
text(5*xlim(2)/10,(ylim(1) + ylim(2))/18,mystr,'Interpreter','latex', 'fontsize',14)
h = lsline;
set(h,'LineWidth', 1)
ylabel('Bounded-Katz')
xlabel('Katz')
[katz, katz_order] = sort(W1,'descend');
[Bound_katz, Bound_katz_order] = sort(W2,'descend');
hold on;
scatter(W1(labelled_nodes), W2(labelled_nodes), 'fill');
hold off;
%%
[[1:n]', katz_order, Bound_katz_order];
%[[1:n]', W1,W2]
%scatter(katz_order, Bound_katz_order)
%%
