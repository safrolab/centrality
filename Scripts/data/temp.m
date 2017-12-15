rng(212)
p = 0.1;
out = zeros(20, 1);
for i=1:20
    new_status = binornd(1,p);
    out(i) = new_status;
end
[[1:20]' out]