out = zeros(n,1);
for i=1:10000
    [soc_katz, katz, labelled_nodes] = SOC_Katz(A, 3, 0.1);
    out = out + soc_katz;
    %install_marker = zeros(n,1);
    %install_marker(labelled_nodes) = 1;
    %filename = strcat('grid20x20_', int2str(i), '.txt');
    %fileID = fopen(filename,'w');
    %y = [katz, soc_katz, install_marker];
    %fprintf(fileID,'%f %f %d\n',y');
    %fclose(fileID);

end
out1 = out/norm(out);
katz1 = katz/norm(katz);
scatter(out1, katz1)