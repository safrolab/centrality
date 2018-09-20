function[recover_list, num_current_recover] = update_new_recovered(recover_list, num_current_recover, nodes_to_add, num_to_add)

add_nodes = nodes_to_add(1:num_to_add);
start_indx = num_current_recover + 1;
stop_indx = num_current_recover + num_to_add;
recover_list(start_indx:stop_indx) = add_nodes;
num_current_recover = num_current_recover + num_to_add;
end