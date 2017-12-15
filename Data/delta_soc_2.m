function[exp_coverage, active_count] = delta_soc_2(G, init_active,p, full_soc, niter, install)
%{
Same as delta_soc with different definition on immunzation
In this model, a node that is immuzited can still spread information
however, it cannot be infected  with a virus that resets it's 
time-to-live counter
%}
out = zeros(niter,1);
out_active = zeros(G.numnodes, niter);
parfor j = 1:niter
    [cov, active] = multi_try_coverage_dir_2(G, init_active,p, full_soc, install);
    out(j) = out(j) + cov;
    out_active(:,j) = active;
    %out(j) = out(j) + multi_try_coverage_dir(G, init_active,p, immune, full_soc, install);
end
exp_coverage = sum(out)/niter;
active_count = out_active*ones(niter,1);
end