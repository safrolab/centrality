%{
Experiment to compare start nodes


%}
nnodes = 10;
out1 = zeros(nnodes, 2);
out2 = zeros(nnodes, 2);
out3 = zeros(nnodes, 2);
out4 = zeros(nnodes, 2);
for j = 1:nnodes
    node_soc = top_soc(j);
    node_deg = top_deg(j);
    cov_soc = 0;
    cov_deg = 0;
    niter = 1000;
    for i=1:1000
        cov_soc = cov_soc + particle_track(G, node_soc, 10, immunize_dic,install_dic, max_time);
        cov_deg = cov_deg + particle_track(G, node_deg, 10, immunize_dic,install_dic, max_time);

    end
    out(j,1) = cov_soc/niter;
    out(j, 2) = cov_deg/niter;
end
out