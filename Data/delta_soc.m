function[exp_coverage, active_count] = delta_soc(G, init_active,p, immune, full_soc, niter, install)
out = zeros(niter,1);
out_active = zeros(G.numnodes, niter);
parfor j = 1:niter
    [cov, active] = multi_try_coverage_dir(G, init_active,p, immune, full_soc, install);
    out(j) = out(j) + cov;
    out_active(:,j) = active;
    %out(j) = out(j) + multi_try_coverage_dir(G, init_active,p, immune, full_soc, install);
end
exp_coverage = sum(out)/niter;
active_count = out_active*ones(niter,1);
end