dat=table2array();
%dat=dat(dat(:,3)<20,:)
%dat(:,3)=~isoutlier(dat(:,3),'median').*dat(:,3);
figure
scatter(dat(:,1),dat(:,2),[],dat(:,3),'filled')
tit="Lens 1 Period 4 Single Pixel 3-23"
title(tit);
colorbar
figure
histogram(dat(:,3))
title(tit)