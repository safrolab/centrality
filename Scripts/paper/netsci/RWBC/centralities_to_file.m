% 1. Read graph from file
% 2. Read s, t, full_soc from file
% 3. Read install nodes from file
% 4. Write standard_st_centrality to file
% 5. Write soc_st_centrality to file

%import data and parameters
nonzeros = importdata('myminnesota_graph.txt');
n = max(size(nonzeros));
A = spconvert([nonzeros ones(n,1)]);
install_nodes = importdata('install_nodes.txt');
s_t_full_soc = importdata('s_t_full_soc.txt');
source = s_t_full_soc(1);
terminal = s_t_full_soc(2);
full_soc = s_t_full_soc(3);
st_array = [source terminal];

% compute centrality scores
standard_cen = standard_st_centrality(A, source, terminal);
standard_cen = standard_cen/norm(standard_cen);

soc_cen = sample_st_randomwalkBC(A, st_array,install_nodes, full_soc);
soc_cen = soc_cen/norm(soc_cen);

% Write centralities to file
fileID = fopen('mycentrality_standard.txt', 'w');
fprintf(fileID,'%12.8f\n', standard_cen);
fclose(fileID);
fileID = fopen('mycentrality_SOC.txt', 'w');
fprintf(fileID,'%12.8f\n', soc_cen);
fclose(fileID);


