function[exp_coverage] = ...
    delta_soc_4(G, start_node, full_soc, immunize_dic, install_dic, ...
    niter, max_time)
%{
Same as delta_soc with different definition on immunzation
In this model, a node that is immuzited can still spread information
however, it cannot be infected  with a virus that resets it's 
time-to-live counter
%}
out = zeros(niter,1);
out_active = zeros(G.numnodes, niter);
parfor j = 1:niter
    coverage = particle_track(G, start_node, full_soc, immunize_dic, ...
    install_dic, max_time);
    out(j) = coverage;
end
exp_coverage = sum(out)/niter;
end