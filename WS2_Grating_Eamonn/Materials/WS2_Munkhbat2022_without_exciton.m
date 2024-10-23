clear all
close all

data=load('WS2_Munkhbat2022.txt');

lambda=data(:,1);
n=data(:,2);
k=data(:,3);

%% n
% figure(78)
% plot(1:length(lambda),n,'r--'); hold on
% plot([174;230;328;(500:length(lambda))'],[n(174);n(230);n(328);n(500:end)],'g'); hold on

% figure(79)
% plot(lambda,n,'r--'); hold on
% plot([lambda(174);lambda(230);lambda(328);lambda(500:end)],[n(174);n(230);n(328);n(500:end)],'g'); hold on

weights=ones(size([n(174);n(230);n(270);n(367:end)],1),1);
weights(1:3)=500;

ft = fittype('a1*exp(-((x-b1)/c1)^2)+d1');
f = fit([lambda(174);lambda(230);lambda(270);lambda(367:end)], [n(174);n(230);n(270);n(367:end)], ft,'startpoint',[2.5 0.551 0.130 3.79],'weight',weights);  
n_fit=f.a1*exp(-((lambda-f.b1)/f.c1).^2)+f.d1;


%% k

figure(80)
plot(1:length(lambda),k,'b--'); hold on
plot([174;230;270;(367:length(lambda))'],[k(174);k(230);k(270);k(367:end)],'g'); hold on

% figure(81)
% plot(lambda,k,'b--'); hold on
% plot([lambda(174);lambda(230);lambda(270);lambda(367:end)],[k(174);k(230);k(270);k(367:end)],'g'); hold on

weights=ones(size([k(174);k(230);k(270);k(367:end)],1),1);
weights(1:3)=500;

ft = fittype('a1*exp(-((x-b1)/c1)^2)+d1');
f = fit([lambda(174);lambda(230);lambda(270);lambda(367:end)], [k(174);k(230);k(270);k(367:end)], ft,'startpoint',[2.5 0.415 0.200 0],'weight',weights);  
k_fit=f.a1*exp(-((lambda-f.b1)/f.c1).^2)+f.d1;


ft = fittype('singleLorentz_line(x,A1,x1,gamma1,a,b)');
f = fit(lambda(322:400), k(322:400), ft,'startpoint',[1.3 0 0 0.050 0.629],'Lower',[0 0 0 0 0.400],'Upper',[10 Inf Inf 100 0.800]);  
k_fit=singleLorentz_line(lambda,f.A1,f.x1,f.gamma1,f.a,f.b);

figure(45)
plot(lambda(322:400), k(322:400),'r'); hold on
plot(lambda(322:400), singleLorentz_line(lambda(322:400),f.A1,f.x1,f.gamma1,f.a,f.b),'r--'); hold on

%% n k

% k_fit=k-k_fit;

figure(81)
plot(lambda,n,'b'); hold on
plot(lambda,n_fit,'b--'); hold on
plot([lambda(1) lambda(end)],[4.65 4.65],'b-.'); hold on
plot(lambda,k,'r'); hold on
plot(lambda,k_fit,'r--'); hold on
plot([lambda(1) lambda(end)],[0 0],'r-.'); hold on
xlim([lambda(1) lambda(end)])
ylim([-0.1 7])
title('n and k WS_2')
xlabel('Energy (eV)')
ylabel('n/k')
set(gca,'TickDir','out','Ycolor','k','Xcolor','k','Linewidth',1.5,'Layer','top','Fontsize',15);
hold off


figure(82)
plot(1.240./lambda,n,'b','Linewidth',2); hold on
plot(1.240./lambda,n_fit,'b--','Linewidth',2); hold on
plot(1.240./[lambda(end) lambda(1)],[4.65 4.65],'b-.','Linewidth',2); hold on
ylabel('n')
ylim([2.9 5.6])
hold on
yyaxis right
plot(1.240./lambda,k,'r','Linewidth',2); hold on
plot(1.240./lambda,k_fit,'r--','Linewidth',2); hold on
plot(1.240./[lambda(end) lambda(1)],[0 0],'r-.','Linewidth',2); hold on
ylabel('k')
ylim([-0.015 2.65])
title('n and k WS_2')
legend('n','n /wo X','n cst','k','k /wo X','k cst','Location','northwest')
% legend('n','n /wo X','k','k /wo X','Location','northwest')
% annotation('arrow',[0.36 0.26],[0.55 0.55],'Linewidth',2)
% annotation('arrow',[0.75 0.85],[0.45 0.45],'Linewidth',2)
xlim([0.8 4.1])
xlabel('Energy (eV)')
set(gca,'TickDir','out','Ycolor','k','Xcolor','k','Linewidth',1.5,'Layer','top','Fontsize',15);
hold off



a=(5.19-4.11)/(2.48-1.54);
b=4.11-a*1.54;
n_fit=a*1.240./lambda+b;

figure(83)
plot(1.240./lambda,n,'b','Linewidth',2); hold on
plot(1.240./lambda,n_fit,'b--','Linewidth',2); hold on
plot(1.240./[lambda(end) lambda(1)],[4.65 4.65],'b-.','Linewidth',2); hold on
ylabel('n')
ylim([4.12 5.32])
hold on
yyaxis right
plot(1.240./lambda,k,'r','Linewidth',2); hold on
plot(1.240./lambda,k_fit,'r--','Linewidth',2); hold on
plot(1.240./[lambda(end) lambda(1)],[0 0],'r-.','Linewidth',2); hold on
ylabel('k')
ylim([-.015 1.44])
title('n and k WS_2')
legend('n','n /wo X','n cst','k','k /wo X','k cst','Location','northwest')
% legend('n','n /wo X','k','k /wo X','Location','northwest')
% annotation('arrow',[0.36 0.26],[0.55 0.55],'Linewidth',2)
% annotation('arrow',[0.75 0.85],[0.45 0.45],'Linewidth',2)
xlabel('Energy (eV)')
xlim([1.54 2.48])
set(gca,'TickDir','out','Ycolor','k','Xcolor','k','Linewidth',1.5,'Layer','top','Fontsize',15);
hold off


data=[lambda,n_fit,k_fit];
data=[lambda,n,k_fit];

% data=[lambda,n_fit,0*k_fit];

