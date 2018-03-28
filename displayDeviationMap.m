dat=table2array(dev)
dat=dat(dat(:,3)<5,:)
%%dat(:,3)=~isoutlier(dat(:,3)).*dat(:,3);
scatter(dat(:,1),dat(:,2),[],dat(:,3),'filled')
title("Lens 2 Period 4 Single Pixel 3-23")
colorbar
figure
histogram(dat(:,3))