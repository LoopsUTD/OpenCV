dat=table2array(dev)
dat=dat(dat(:,3)<5,:)
%%dat(:,3)=~isoutlier(dat(:,3)).*dat(:,3);
scatter(dat(:,1),dat(:,2),[],dat(:,3),'filled')
colorbar
figure
histogram(dat(:,3))