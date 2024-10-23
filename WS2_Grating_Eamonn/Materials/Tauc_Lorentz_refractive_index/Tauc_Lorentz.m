function [n,k]=Tauc_Lorentz_fit(x,Eg,eps_inf,A1,C1,E01,A2,C2,E02)
%                                                A3,C3,E03,A4,C4,E04,...
%                                                A5,C5,E05,A6,C6,E06,...
%                                                A7,C7,E07,A8,C8,E08)

E_sim=0:0.01:18; % E must be equispaced                                   
Emin=E_sim(1);
Emax=E_sim(end);
N=1+100*(floor(Emax-Emin));                                   
eps2=zeros(N,1);
M=0;

for  E_sim=Emin:0.01:Emax
M=M+1;

if E_sim>Eg 
osc1_imag=(A1*E01*C1*(E_sim-Eg)^2)/(E_sim*((E_sim^2-E01^2)^2+(C1*E_sim)^2));
osc2_imag=(A2*E02*C2*(E_sim-Eg)^2)/(E_sim*((E_sim^2-E02^2)^2+(C2*E_sim)^2));
% osc3_imag=(A3*E03*C3*(E_sim-Eg)^2)/(E_sim*((E_sim^2-E03^2)^2+(C3*E_sim)^2));
% osc4_imag=(A4*E04*C4*(E_sim-Eg)^2)/(E_sim*((E_sim^2-E04^2)^2+(C4*E_sim)^2));
% osc5_imag=(A5*E05*C5*(E_sim-Eg)^2)/(E_sim*((E_sim^2-E05^2)^2+(C5*E_sim)^2));
% osc6_imag=(A6*E06*C6*(E_sim-Eg)^2)/(E_sim*((E_sim^2-E06^2)^2+(C6*E_sim)^2));
% osc7_imag=(A7*E07*C7*(E_sim-Eg)^2)/(E_sim*((E_sim^2-E07^2)^2+(C7*E_sim)^2));
% osc8_imag=(A8*E08*C8*(E_sim-Eg)^2)/(E_sim*((E_sim^2-E08^2)^2+(C8*E_sim)^2));

else
osc1_imag=0;
osc2_imag=0;  
% osc3_imag=0;
% osc4_imag=0; 
% osc5_imag=0;
% osc6_imag=0; 
% osc7_imag=0;
% osc8_imag=0; 
end

eps2(M)=osc1_imag+osc2_imag;
% eps2(M)=osc1_imag+osc2_imag+osc3_imag+osc4_imag+osc5_imag+osc6_imag+osc7_imag+osc8_imag;
     
end

E_sim=Emin:0.01:Emax;
eps1=kkrebook(E_sim,eps2,0)+eps_inf;
eps1=eps1';
n=sqrt(0.5*(sqrt(eps1.^2+eps2.^2)+eps1));
k=sqrt(0.5*(sqrt(eps1.^2+eps2.^2)-eps1));

n=interp1(E_sim,n,x);
k=interp1(E_sim,k,x);
                                                                                                                                         
end
                                    
                                    
