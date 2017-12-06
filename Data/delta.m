function[exp_coverage] = delta(G, init_active,p, niter)
out = 0;
for i = 1:niter
    out = out + infection_cascade_mod(G, init_active,p);
end
exp_coverage = out/niter;
end