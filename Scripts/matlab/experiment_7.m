function [] = experiment_7(G)
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
install_choice = [0.99, 0.2, 0.4];
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
        steps = 3;
        num_install = ceil(install_percentage*n);
        install = randsample(n, num_install);
        install_dic = zeros(n,1);
        install_dic(install) = 1;
        soc_katz = SOC_Katz_install_nodes(A, steps, num_install, install);
        %compute coverage for each node
        num_try = 1000;
        max_time = n;
        %hop_limit = 10;
        p =0.03;
        base_centrality = zeros(n,1);
        num_sample_nodes = 1000;
        sample_nodes = randsample(n, num_sample_nodes);
        for ind=1:num_sample_nodes
            ind
            node = sample_nodes(ind);
            exp_coverage= delta(G, [node],p, num_try);
            base_centrality(node) = exp_coverage;
            %exp_coverage
            %nnz(base_centrality)
        end
        sample_soc = soc_katz(sample_nodes);
        sample_katz = katz(sample_nodes);
        sample_deg = degree(sample_nodes);
        sample_base =  base_centrality(sample_nodes);

        soc_rank = node_rank(sample_soc, num_sample_nodes);
        katz_rank = node_rank(sample_katz, num_sample_nodes);
        deg_rank = node_rank(sample_deg, num_sample_nodes);
        base_rank = node_rank(sample_base, num_sample_nodes);
        [rho_soc, p_soc] = corr(soc_rank, base_rank, 'type', 'Kendall');
        [rho_katz, p_katz] = corr(katz_rank, base_rank, 'type', 'Kendall');
        [rho_deg, p_deg] = corr(deg_rank, base_rank, 'type', 'Kendall');
        %[sample_soc, sample_katz, sample_deg, sample_base]
        %[soc_rank, katz_rank, deg_rank, base_rank]
        [deg_rank sample_deg]
        %scatter(sample_deg, sample_base)
        scatter(deg_rank, base_rank)
    
%{
        nz_degree_nodes = find(degree);
        [nnz_deg_nodes, ~] = size(nz_degree_nodes);
        soc_nodes = soc_katz(nz_degree_nodes);
        katz_nodes = katz(nz_degree_nodes);
        deg_nodes = degree(nz_degree_nodes);
        base_nodes = base_centrality(nz_degree_nodes);
        [~, soc_rank] = sort(soc_nodes, 'descend');
        [~, katz_rank] = sort(katz_nodes, 'descend');
        noise = rand(nnz_deg_nodes,1)./10;
        [~, deg_rank] = sort(deg_nodes + noise, 'descend');
        [~,base_rank] = sort(base_nodes, 'descend');
        [rho_soc, p_soc] = corr(soc_rank, base_rank, 'type', 'Spearman');
        [rho_katz, p_katz] = corr(katz_rank, base_rank, 'type', 'Spearman');
        [rho_deg, p_deg] = corr(deg_rank, base_rank, 'type', 'Spearman');
%}
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
