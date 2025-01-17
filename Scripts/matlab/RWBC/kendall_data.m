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
%deg_cen = A*ones(n,1);
%[~, sort_nodes] = sort(deg_cen, 'descend');
%[~, sort_nodes] = sort(deg_cen);

%idx = randperm(n);
%A = A(idx, :);
%A = A(:,idx);
%A= A+A';
%A = Problem.A;
fileID = fopen('minnesota_current_flow_centrality.txt','r');
formatSpec = '%f';
current_flow = fscanf(fileID,formatSpec);
A(A>0) = 1;
install_percentage = 0.2;
[~, n] = size(A);
num_labelled_nodes = ceil(install_percentage*n);

%fileID = fopen('rwbc_table.txt','a');
%%
for steps = [10]
for i=1:1
    labelled_nodes = randperm(n,num_labelled_nodes);
    %v = get_soc_katz(A, steps, labelled_nodes,p);
    centrality = SOC_RWBC( A, steps, labelled_nodes );
    %v = round(v, 6);
    %[~, ix] = sort(v, 'descend');
    %soc_rank = 1:n;
    %soc_rank(ix) = soc_rank;
    %ken = corr(katz_rank', soc_rank', 'Type', 'Kendall');
    %out = [p install_percentage steps ken];
  
    %fprintf(fileID,'grid10 %f %f %d %f\n',out');
end
%[current_flow, centrality]
end
 %fclose(fileID);
    
