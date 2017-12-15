function [counter] = experiment_6(G)
%{
Experiment compares soc_katz, katz and degree. It tries to identify 
which centrality is best used to indentify top particle spread
1. Computer Katz, and degree centrality
2. Choose install_percentage
3 a. Random install k
3 b. Compute soc_katz
3 c. Compute coverage for each node: cover_cen centrality
3 d. Rank Stats: soc Vs cover_cen, katz Vs cover_cen, deg Vs cover_cen
            spearmans correlation (r_soc, r_katz, r_deg)
4 a. Repeat 3, 1000 times
4 b. Plot sorted r values for install_percentage
5. Repeat 2 for install_percentage = 0.01, 0.05, 0.1, 0.2, 0.4
%}
myCluster=parcluster('local');
%parpool(myCluster,myCluster.NumWorkers);
A = G.adjacency;
n = G.numnodes;
%P = speye(n);
%P = P(randperm(n),:);
%A = P*A*P';
%G = digraph(A);
%n = G.numnodes;
katz = Katz(A);
degree = G.outdegree;

%
n_trials = 1;
install_choice = [0.9, 0.2, 0.4];
fileID = fopen('rho.txt','w');
com = '#install \t r_soc \t r_katz \t r_deg \n';
fprintf(fileID,com);
fclose(fileID);
fileID = fopen('pval.txt','w');
com = '#install  p_soc p_katz  p_deg \n';
fprintf(fileID,com);
fclose(fileID);
for x = 1:1
    install_percentage= install_choice(x);
    for j =1:n_trials
        [j, j]
        %install_percentage = 0.1;
        steps = 5;
        num_install = ceil(install_percentage*n);
        install = randsample(n, num_install);
        install_dic = zeros(n,1);
        install_dic(install) = 1;
        soc_katz = SOC_Katz_install_nodes(A, steps, num_install, install);
        %compute coverage for each node
        num_rand_start = 10000;
        max_time = n;
        hop_limit = 10;
        counter = exp_traffic_count(G, hop_limit, install_dic, ...
            max_time, num_rand_start);
        
        nz_degree_nodes = find(degree);
        [nnz_deg_nodes, ~] = size(nz_degree_nodes);
        soc_nodes = soc_katz(nz_degree_nodes);
        katz_nodes = katz(nz_degree_nodes);
        deg_nodes = degree(nz_degree_nodes);
        traffic_nodes = counter(nz_degree_nodes);
        [~, soc_rank] = sort(soc_nodes, 'descend');
        [~, katz_rank] = sort(katz_nodes, 'descend');
        noise = rand(nnz_deg_nodes,1)./10;
        [~, deg_rank] = sort(deg_nodes + noise, 'descend');
        [~,traffic_rank] = sort(traffic_nodes, 'descend');
        [rho_soc, p_soc] = corr(soc_rank, traffic_rank, 'type', 'Spearman');
        [rho_katz, p_katz] = corr(katz_rank, traffic_rank, 'type', 'Spearman');
        [rho_deg, p_deg] = corr(deg_rank, traffic_rank, 'type', 'Spearman');
        rho = [x, rho_soc, rho_katz, rho_deg]
        pval = [x, p_soc, p_katz, p_deg];
        fileID = fopen('rho.txt','a');
        fmt = '%d %5.4f %5.4f %5.4f\n'; 
        fprintf(fileID,fmt, rho);
        fclose(fileID);
        fileID = fopen('pval.txt','a');
        fmt = '%d %5.4f %5.4f %5.4f\n'; 
        fprintf(fileID,fmt, pval);
        fclose(fileID);
    end
end
end
