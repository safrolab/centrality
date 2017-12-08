function[exp_soc_katz] = Exp_SOC_Katz(A, steps, install_percentage, niter)
[~, n] = size(A);
out = zeros(n,1);
parfor i=1:niter
    i
    soc_katz = SOC_Katz(A,steps, install_percentage);
    out = out + soc_katz;
end
exp_soc_katz= out/norm(out);
end