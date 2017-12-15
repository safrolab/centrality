function[exp_coverage] = delta(G, init_active,p, niter)
out = zeros(niter,1);
for i = 1:niter
    out(i) = out(i) + infection_cascade_mod(G, init_active,p);
end
exp_coverage = sum(out)/niter;
end