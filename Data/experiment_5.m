function [] = experiment_5(G)
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
n_trials = 10;
install_choice = [0.1, 0.2, 0.4];
fileID = fopen('rho.txt','w');
com = '#install \t r_soc \t r_katz \t r_deg \n';
fprintf(fileID,com);
fclose(fileID);
fileID = fopen('pval.txt','w');
com = '#install  p_soc p_katz  p_deg \n';
fprintf(fileID,com);
fclose(fileID);
for x = 1:3
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
        node_coverage = zeros(n,1);
        niter = 200;
        max_time = n;
        hop_limit = 20;
        parfor start_node=1:n
            if degree(start_node) > 0
                exp_spread = exp_particle_spread(G, start_node, hop_limit,...
                                install_dic, max_time, niter);  
                 
                node_coverage(start_node) = exp_spread;
                %exp_spread
            else
                node_coverage(start_node) = 1;
            end
        end
        nz_degree_nodes = find(degree);
        [nnz_deg_nodes, ~] = size(nz_degree_nodes);
        soc_nodes = soc_katz(nz_degree_nodes);
        katz_nodes = katz(nz_degree_nodes);
        deg_nodes = degree(nz_degree_nodes);
        cov_nodes = node_coverage(nz_degree_nodes);
        [~, soc_rank] = sort(soc_nodes, 'descend');
        [~, katz_rank] = sort(katz_nodes, 'descend');
        noise = rand(nnz_deg_nodes,1)./10;
        [~, deg_rank] = sort(deg_nodes + noise, 'descend');
        [~, cov_rank] = sort(cov_nodes, 'descend');
        [rho_soc, p_soc] = corr(soc_rank, cov_rank, 'type', 'Spearman');
        [rho_katz, p_katz] = corr(katz_rank, cov_rank, 'type', 'Spearman');
        [rho_deg, p_deg] = corr(deg_rank, cov_rank, 'type', 'Spearman');
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
