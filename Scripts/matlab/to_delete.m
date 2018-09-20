Test1 = wrc;
Test2 = wsc;
bins = 30;
figure
[counts1, values1] = hist(Test1(:), bins);
[counts2, values2] = hist(Test2(:), bins);
bar(values1, counts1,'r');
hold on
bar(values2, counts2,'b');
legend('RWBC', 'S-RWBC')


%%
Test1 = wrc;
Test2 = wsc;
hold on
h1 = histfit(Test1, 30);
set(h1(2),'color','r')
h2 = histfit(Test2, 30);
set(h2(2),'color','b')
%delete(h1(1));
%delete(h2(1));
hold off