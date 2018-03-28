dat=table2array(lens6)
dat=dat(dat(:,3)<15,:)
%%dat(:,3)=~isoutlier(dat(:,3)).*dat(:,3);
figure
scatter(dat(:,1),dat(:,2),[],dat(:,3),'filled')
title("Lens 3 Period 4 Single Pixel 3-23")
colorbar
figure
histogram(dat(:,3))