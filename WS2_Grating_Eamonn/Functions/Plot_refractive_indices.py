# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 10:31:48 2022

@author: ph1pbx
"""

def Plot_refractive_indices(lbda,material):

    import matplotlib.pyplot as plt
    from Functions.get_anisotropic_permittivities import get_anisotropic_permittivities
    from Functions.epsilon2n import epsilon2n

    permittivity_xx,permittivity_yy,permittivity_zz=get_anisotropic_permittivities(lbda,material)   # Set the materials permitivitties                                   

    for m in range(0,len(material)):
      
        fig, axs = plt.subplots(2, 1, sharex=True, figsize=(10, 15), dpi=80)
        
        if isinstance(material[m], str):
            ttl =fig.suptitle(material[m][10:-4])  
        else:
            ttl =fig.suptitle(str(material[m][0])+str('+')+str(material[m][1])+str('i'))   
        ttl.set_position([.5, 0.89])
    
        twin0 = axs[0].twinx()
        p1=axs[0].plot(lbda,permittivity_zz.real[:,m], "#03a9fc",lbda,permittivity_xx.real[:,m], "b-",lbda,permittivity_yy.real[:,m], "b-") 
        p2=twin0.plot(lbda,permittivity_zz.imag[:,m], "#f54927",lbda,permittivity_xx.imag[:,m], "r-",lbda,permittivity_yy.imag[:,m], "r-")
        # plt.text(0.5,0.5,'zz')
        axs[0].set_ylabel("$\epsilon_r$")
        twin0.set_ylabel("$\epsilon_i$")
        axs[0].spines['left'].set_color('blue')
        axs[0].tick_params(axis='y', colors='blue')
        axs[0].yaxis.label.set_color('blue')
        twin0.spines['right'].set_color('red')
        twin0.tick_params(axis='y', colors='red')
        twin0.yaxis.label.set_color('red')
    
        nxx,kxx,nyy,kyy,nzz,kzz=epsilon2n(permittivity_xx.real[:,m],permittivity_xx.imag[:,m],permittivity_yy.real[:,m],permittivity_yy.imag[:,m],permittivity_zz.real[:,m],permittivity_zz.imag[:,m])
    
        twin1 = axs[1].twinx()
        p1=axs[1].plot(lbda,nzz,"#03a9fc",lbda,nxx,"b-",lbda,nyy, "b-") 
        p2=twin1.plot(lbda,kzz, "#f54927",lbda,kxx, "r-",lbda,kyy, "r-")
        axs[1].set_xlabel("wavelength($\mu$m)")
        axs[1].set_ylabel("$n$")
        axs[1].set_ylim(0.9*min(min(nzz),min(nyy),min(nxx)),1.1*max(max(nzz),max(nyy),max(nxx)))
        twin1.set_ylabel("$k$")
        axs[1].spines['right'].set_color('blue')
        axs[1].tick_params(axis='y', colors='blue')
        axs[1].yaxis.label.set_color('blue')
        twin1.spines['right'].set_color('red')
        twin1.tick_params(axis='y', colors='red')
        twin1.yaxis.label.set_color('red')
    
        pos01 = axs[0].get_position()
        pos02 = [pos01.x0 , pos01.y0-0.04 ,  pos01.width , 1.03*pos01.height] 
        pos11 = axs[1].get_position()
        pos12 = [pos11.x0 , pos11.y0 ,  pos11.width , 1.03*pos11.height] 
        axs[0].set_position(pos02)
        axs[1].set_position(pos12)
        
        plt.rc('font', size=12)          # controls default text sizes

        plt.show()