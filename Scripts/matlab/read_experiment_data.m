function[B] = read_experiment_data()
%{
data to read:
    1. graphfile
    2. sourcenodes
    3. st pairs
    4. install_nodes
    5. walks
%}
myCluster=parcluster('local');
parpool(myCluster,myCluster.NumWorkers);
%load('davis_southern_women_graph.mat'); <- DO NOT LOAD, index problem
%A = davis_southern_women_graph();
[A] = edgefile2mat('p2p-Gnutella08.txt');
A(A >0) = 1;

%A(A>0) = 1;
full_soc = 3;
%  read files from dir
%mydir = ['/home/hushiji/Research/centrality/'...
%'Scripts/python_scripts/congestion/pre_data/example/randomwalks/'];
mydir = ['/home/hushiji/Research/centrality/'...
'Scripts/python_scripts/congestion/pre_data/p2p-Gnutella08/randomwalks/'];
files = dir(strcat(mydir, '*.txt'));
[no_pair_files, ~] = size(files);
no_pair_files = no_pair_files/2; %two types of .txt files for each case
ratio_scene = zeros(no_pair_files, 2);
row = 1;
for file = files'  % what files are in local dir 
    if file.name(1:7) == 'install'
        r_s = regexp(file.name,'\d*','Match');
        ratio_scene(row, 1) = str2num(cell2mat(r_s(1)));
        ratio_scene(row, 2) = str2num(cell2mat(r_s(2)));
        row = row + 1;
    end
end
%install_nodes
%st_pairs
%katzdir  = ['/home/hushiji/Research/centrality/'...
%'Scripts/python_scripts/congestion/post_data/example/randomwalks/'];
katzdir  = ['/home/hushiji/Research/centrality/'...
'Scripts/python_scripts/congestion/post_data/p2p-Gnutella08/randomwalks/'];
parfor row = 1:no_pair_files
    ratio = num2str(ratio_scene(row, 1));
    scenario = num2str(ratio_scene(row, 2));
    filetag = strcat(ratio, '_',scenario, '.txt');
    installfile = strcat(mydir, 'install', filetag);
    stfile = strcat(mydir, 'source_target', filetag);
    st_array = load(stfile);
    install_array = load(installfile);
    st_array = st_array + 1;  % MATLAB indexing from python
    install_array  = install_array + 1;
    [ratio, scenario]
    [centrality, ~] = sample_st_randomwalkBC(A, st_array,...
    install_array, full_soc);
    katzfile = strcat(katzdir, 'RWBC',filetag);
    fileID = fopen(katzfile, 'w');
    fprintf(fileID,'%f\n',centrality);
    fclose(fileID);
end
%[n, ~]= size(centrality);
%[[0:n-1]' centrality];
end
