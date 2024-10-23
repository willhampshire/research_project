function [n,k]=n_k_MAPB(E,Eg,Q2B,eps_inf,A1,C1,E01,A2,C2,E02)

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
else
osc1_imag=0;
osc2_imag=0;   
end

eps2(M)=Q2B+osc1_imag+osc2_imag;
     
end

E_sim=Emin:0.01:Emax;
eps1=kkrebook(E_sim,eps2,0)+eps_inf;
eps1=eps1';
n=sqrt(0.5*(sqrt(eps1.^2+eps2.^2)+eps1));
k=sqrt(0.5*(sqrt(eps1.^2+eps2.^2)-eps1));

n=interp1(E_sim,n,E);
k=interp1(E_sim,k,E);
                                                                                                                                         
end
                                    
                                    
