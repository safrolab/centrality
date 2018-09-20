%formatSpec = '%d %d';
%sizeA = [2 Inf];
%edgefile = 'out.ego-facebook';
%fileID = fopen(edgefile, 'r');
%edges = fscanf(fileID, formatSpec, sizeA);
%A = sparse(edges(:,1), edges(:,2),1, n,n);
%A = A + A';
%load('ca-GrQc.mat');
%delimiterIn = ' ';
%headerlinesIn = 2;
%edges = importdata('out.moreno_health_health', delimiterIn,headerlinesIn);
%edges = importdata('out.ego-facebook', delimiterIn,headerlinesIn);
%edges = edges.data;
%n = max(max(edges(:,1:2)));
%A = sparse(edges(:,1), edges(:,2),1, n,n);
[~, n] = size(A);
deg_cen = A*ones(n,1);
%[~, sort_nodes] = sort(deg_cen, 'descend');
[~, sort_nodes] = sort(deg_cen);

idx = randperm(n);
A = A(idx, :);
A = A(:,idx);
%A= A+A';
%A = Problem.A;
A(A>0) = 1;
mysteps = [2,2,2,2,2,2];
p = 0.2;
install_percentage = 0.2;
katz_cen = Katz(A, p);
katz_cen = round(katz_cen, 6);
[~, ix] = sort(katz_cen, 'descend');
katz_rank = 1:n;
katz_rank(ix) = katz_rank;
[~, n] = size(A);
c = A*ones(n,1);
[~, nodes] = sort(c);
num_labelled_nodes = ceil(install_percentage*n);
%num_choices = ceil(0.8*n);
%install_nodes = [10 20 50];
%labelled_nodes = randperm(n,num_labelled_nodes);
fileID = fopen('exptable.txt','a');
for steps = [2 4 6 8 10 12 14 16];
for i=1:30
    %steps = 3;
    
    labelled_nodes = randperm(n,num_labelled_nodes);
    %labelled_nodes = sort_nodes(1:install_nodes(i));
    %perm = randperm(num_choices,num_labelled_nodes);
    %labelled_nodes = nodes(perm);
    %p = 0.05;
    v = get_soc_katz(A, steps, labelled_nodes,p);
    v = round(v, 6);
    [~, ix] = sort(v, 'descend');
    soc_rank = 1:n;
    soc_rank(ix) = soc_rank;
    ken = corr(katz_rank', soc_rank', 'Type', 'Kendall');
    out = [p install_percentage steps ken];
  
    fprintf(fileID,'grid10 %f %f %d %f\n',out');
end
end
 fclose(fileID);
    