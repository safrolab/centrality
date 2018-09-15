function[st_cen_A] = get_flow_vec( st_cen_B, n, steps)
st_cen_A = zeros(n,1);
for node=1:n
    st_cen_A_node =  0;
    for i=1:steps
        st_cen_A_node = st_cen_A_node + st_cen_B(node + (i-1)*steps);
    end
    st_cen_A(node) = st_cen_A_node;
end

end
