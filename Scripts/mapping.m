function [V_t_pos] = mapping(i, t, n)
b = ceil(i/n);
r = mod(i-1,n) + 1;

if  r < t
    V_t_pos = i - (b-1);
elseif r > t
    V_t_pos = i - b;
else
    V_t_pos = 0;
end
end

    
    
