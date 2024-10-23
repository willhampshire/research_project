clear all

load('cSi_Green_2008.txt')
load('Si_Customized.txt')

figure()
subplot(1,2,1)
plot(cSi_Green_2008(:,1),cSi_Green_2008(:,2),'b','linewidth',2);hold on
plot(Si_Customized(:,1),Si_Customized(:,2),'color',[0 0.3 1],'linewidth',2);hold on
title('Real(n_{Si})')
ylabel('Real(n_{Si})')
xlabel('wavelength (µm)')
xlim([0.25 1.4])
set(gca,'Layer','top','TickDir','out','Linewidth',1.5,'Fontsize',15,'Fontname','Times New Roman');

subplot(1,2,2)
plot(cSi_Green_2008(:,1),cSi_Green_2008(:,3),'r','linewidth',2);hold on;
plot(Si_Customized(:,1),Si_Customized(:,3),'color',[1 0.3 0],'linewidth',2);hold on;
title('Im(n_{Si})')
ylabel('Im(n_{Si})')
xlabel('wavelength (µm)')
xlim([0.25 1.4])
set(gca,'Layer','top','TickDir','out','Linewidth',1.5,'Fontsize',15,'Fontname','Times New Roman');

