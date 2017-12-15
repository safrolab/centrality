function [] = experiment_8(G)
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
install_choice = [0.05, 0.1, 0.2, 0.4];
fileID = fopen('rho.txt','w');
com = '#install \t r_soc \t r_katz \t r_deg \n';
fprintf(fileID,com);
fclose(fileID);
fileID = fopen('pval.txt','w');
com = '#install  p_soc p_katz  p_deg \n';
fprintf(fileID,com);
fclose(fileID);
fileID = fopen('spearman_rho.txt','w');
com = '#install prob r_soc r_katz r_deg \n';
fprintf(fileID,com);
fclose(fileID);
probability = [0.01, 0.02, 0.04, 0.08, 0.1, 0.2, 0.4];

rand_seed = randi(10000);
rng(rand_seed)
for p=probability
    for x = 1:4
        install_percentage= install_choice(x);
        for j =1:n_trials
            [j, j]
            %install_percentage = 0.1;
            steps = 5;
            num_install = ceil(install_percentage*n);
            install = randsample(n, num_install);
            install_dic = zeros(n,1);
            install_dic(install) = 1;
            [soc_katz, ~] = SOC_Katz_install_nodes(A, steps, num_install, install, p);
            %compute coverage for each node
            num_try = 1000;
            max_time = n;
            %hop_limit = 10;
            %p =0.05;
            %p = alpha;
            base_centrality = zeros(n,1);
            num_sample_nodes = 500;
            sample_nodes = randsample(n, num_sample_nodes);
            is_susceptible = zeros(n,1);
            is_susceptible(install) = 1;
            for ind=1:num_sample_nodes
                node = sample_nodes(ind);
                [active, ~] = exp_susceptible_spread(G, node, ...
                                steps, p, is_susceptible, num_try);
                %[exp_coverage, ~] = delta_soc_2(G, [node],p, steps, num_try, install);
                %exp_coverage= delta(G, [node],p, num_try);
                %base_centrality(node) = exp_coverage;
                base_centrality(node) = active;
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

            [sp_rho_soc, ~] = corr(soc_rank, base_rank, 'type', 'Spearman');
            [sp_rho_katz, ~] = corr(katz_rank, base_rank, 'type', 'Spearman');
            [sp_rho_deg, ~] = corr(deg_rank, base_rank, 'type', 'Spearman');
            %[sample_soc, sample_katz, sample_deg, sample_base]
            %[soc_rank, katz_rank, deg_rank, base_rank]
            %[deg_rank sample_deg]
            %scatter(sample_deg, sample_base)
            %scatter(soc_rank, base_rank)



            rho = [install_percentage, p, rho_soc, rho_katz, rho_deg];
            spear_rho = [install_percentage, p, sp_rho_soc, sp_rho_katz, sp_rho_deg];
            pval = [install_percentage, p_soc, p_katz, p_deg];
            fileID = fopen('rho.txt','a');
            fmt = '%5.4 %5.4f %5.4f %5.4f %5.4f\n'; 
            fprintf(fileID,fmt, rho);
            fclose(fileID);
            fileID = fopen('spearman_rho.txt','a');
            fmt = '%5.4f %5.4f %5.4f %5.4f %5.4f\n'; 
            fprintf(fileID,fmt, spear_rho);
            fclose(fileID);
            fileID = fopen('pval.txt','a');
            fmt = '%5.4 %5.4f %5.4f %5.4f %5.4f\n'; 
            fprintf(fileID,fmt, pval);
            fclose(fileID);
        end
    end
end
end
