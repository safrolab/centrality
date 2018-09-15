function[] = read_install_get_katz()
%{
This script reads install nodes from '/pre_data/tech-routers-rf/'
Computes soc_katz centrality and writes to '/post_data/tech-routers-rf/'
%}
[A] = edgefile2mat('tech-routers-rf.txt');
A = A + A';
A(A>0) = 1;
full_soc = 5;
p = 0.03;
mydir = ['/home/hushiji/Research/centrality/'...
'Scripts/python_scripts/congestion/pre_data/tech-routers-rf/'];
files = dir(strcat(mydir, '*.txt'));
[no_pair_files, ~] = size(files);
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
katzdir  = ['/home/hushiji/Research/centrality/'...
'Scripts/python_scripts/congestion/post_data/tech-routers-rf/'];
for row = 1:no_pair_files
    ratio = num2str(ratio_scene(row, 1));
    scenario = num2str(ratio_scene(row, 2));
    filetag = strcat(ratio, '_',scenario, '.txt');
    installfile = strcat(mydir, 'install', filetag);
    install_array = load(installfile);
    [ratio, scenario]
    [num_labelled_nodes, ~] = size(install_array);
    assert(num_labelled_nodes > 1, 'incorrect size num_labelled_nodes');
    [centrality, ~] = SOC_Katz_install_nodes(A, ...
        full_soc, num_labelled_nodes, install_array, p);
    katzfile = strcat(katzdir, 'sockatz',filetag);
    fileID = fopen(katzfile, 'w');
    fprintf(fileID,'%f\n',centrality);
    fclose(fileID);
end
end