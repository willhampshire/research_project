clear all 
close all

Nfig=1;

E=0.5:0.001:4;

n0=4.5*E./E;
k0=0*E./E;

[nX,kX]=Lorentz_3_osc(E,4.5.^2,...
              0,0,0,...
              1.3,0.05,1.97,...
               0,0,0);

[nX,kX]=Lorentz_3_osc(E,4.5.^2,...
              0,0,0,...
              1,0.015,1.97,...
               0,0,0);
nXBG=nX;
kXBG=kX+5*heaviside(E-2.05).*(E-2.05).^.5;

load('WS2_Munkhbat2022.txt')

if ishandle(Nfig)
close(Nfig)
end
figure(Nfig)
plot(1.240./WS2_Munkhbat2022(:,1),WS2_Munkhbat2022(:,2),'b--','Linewidth',2);hold on;
plot(E,n0,'b','Linewidth',2);hold on;
plot(E,nX,'b','Linewidth',2);hold on;
plot(E,nXBG,'b','Linewidth',2);hold on;
ylabel('n_{MAPB}')
hold on
title('n')
legend('n','k')
ylabel('n')
xlabel('Energy (eV)')
xlim([1.6 2.4])
set(gca,'TickDir','out','Ycolor','k','Xcolor','k','Linewidth',1.5,'Layer','top','Fontsize',15);
hold off

Nfig=Nfig+1;

if ishandle(Nfig)
close(Nfig)
end
figure(Nfig)
plot(1.240./WS2_Munkhbat2022(:,1),WS2_Munkhbat2022(:,3),'r--','Linewidth',2);hold on;
plot(E,k0,'r','Linewidth',2);hold on;
plot(E,kX,'r','Linewidth',2);hold on;
plot(E,kXBG,'r','Linewidth',2);hold on;
title('k')
ylabel('k')
xlabel('Energy (eV)')
xlim([1.6 2.4])
set(gca,'TickDir','out','Ycolor','k','Xcolor','k','Linewidth',1.5,'Layer','top','Fontsize',15);
hold off

Nfig=Nfig+1;

Example_0=[1.240./E',n0',k0'];
Example_X=[1.240./E',nX',kX'];
Example_XBG=[1.240./E',nXBG',kXBG'];

% if ishandle(Nfig)
% close(Nfig)
% end
% figure(Nfig)
% plot(1.240./WS2_Munkhbat2022(:,1),WS2_Munkhbat2022(:,2),'b--','Linewidth',2);hold on;
% plot(E,n,'b','Linewidth',2);hold on;
% ylabel('n')
% hold on
% yyaxis right
% plot(1.240./WS2_Munkhbat2022(:,1),WS2_Munkhbat2022(:,3),'r--','Linewidth',2);hold on;
% plot(E,k,'r','Linewidth',2);hold on;
% title('n and k')
% legend('n','k')
% ylabel('k_{MAPB}')
% annotation('arrow',[0.3 0.2],[0.65 0.65],'Linewidth',2)
% annotation('arrow',[0.45 0.55],[0.65 0.65],'Linewidth',2)
% xlabel('Energy (eV)')
% xlim([1.6 2.4])
% set(gca,'TickDir','out','Ycolor','k','Xcolor','k','Linewidth',1.5,'Layer','top','Fontsize',15);
% hold off
% 
% Nfig=Nfig+1;
% 
% if ishandle(Nfig)
% close(Nfig)
% end
% figure(Nfig)
% plot(1.240./WS2_Munkhbat2022(:,1),WS2_Munkhbat2022(:,2),'b--','Linewidth',2);hold on;
% plot(E,n,'b','Linewidth',2);hold on;
% ylabel('n')
% hold on
% yyaxis right
% plot(1.240./WS2_Munkhbat2022(:,1),WS2_Munkhbat2022(:,3),'r--','Linewidth',2);hold on;
% plot(E,k,'r','Linewidth',2);hold on;
% title('n and k')
% legend('n','k')
% ylabel('k_{MAPB}')
% annotation('arrow',[0.3 0.2],[0.65 0.65],'Linewidth',2)
% annotation('arrow',[0.45 0.55],[0.65 0.65],'Linewidth',2)
% xlabel('Energy (eV)')
% xlim([min(E) max(E)])
% set(gca,'TickDir','out','Ycolor','k','Xcolor','k','Linewidth',1.5,'Layer','top','Fontsize',15);
% hold off
% 
% Nfig=Nfig+1;