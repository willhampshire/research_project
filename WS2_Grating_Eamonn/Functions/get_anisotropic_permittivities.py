# -*- coding: utf-8 -*-
"""
Created on Mon May 30 17:37:51 2022

@author: ph1pbx
"""

def get_anisotropic_permittivities(lbda,material):
    
    import numpy as np
    
    permittivity_xx=np.zeros((lbda.size,len(material)),dtype=complex)
    permittivity_yy=np.zeros((lbda.size,len(material)),dtype=complex)
    permittivity_zz=np.zeros((lbda.size,len(material)),dtype=complex)
    
    for m in range(0,len(material)):        
        if isinstance(material[m], str):        
            mat_refractive_index=np.genfromtxt(fname=material[m])
            check=np.diff(mat_refractive_index[:,0]) # check if the wavelength is decreasing
            if check[1]<0:
                mat_refractive_index=np.flipud(mat_refractive_index)
            if len(mat_refractive_index[0])>3: # The material is asinotropic
                nxx=np.interp(lbda,mat_refractive_index[:,0],mat_refractive_index[:,1])
                kxx=np.interp(lbda,mat_refractive_index[:,0],mat_refractive_index[:,2])
                nyy=np.interp(lbda,mat_refractive_index[:,0],mat_refractive_index[:,3])
                kyy=np.interp(lbda,mat_refractive_index[:,0],mat_refractive_index[:,4])
                nzz=np.interp(lbda,mat_refractive_index[:,0],mat_refractive_index[:,5])
                kzz=np.interp(lbda,mat_refractive_index[:,0],mat_refractive_index[:,6])
            else:
                nxx=np.interp(lbda,mat_refractive_index[:,0],mat_refractive_index[:,1])
                nyy=nxx
                nzz=nxx
                kxx=np.interp(lbda,mat_refractive_index[:,0],mat_refractive_index[:,2])
                kyy=kxx
                kzz=kxx
            permittivity_xx[:,m]=(nxx+1j*kxx)**2
            permittivity_yy[:,m]=(nyy+1j*kyy)**2
            permittivity_zz[:,m]=(nzz+1j*kzz)**2
        else:
            if len(material[m])>2: # The material is asinotropic
                nxx=material[m][0]
                kxx=material[m][1]
                nyy=material[m][2]
                kyy=material[m][3]
                nzz=material[m][4]
                kzz=material[m][5]
            else:
                nxx=material[m][0]
                nyy=nxx
                nzz=nxx
                kxx=material[m][1]
                kyy=kxx
                kzz=kxx
            for lb in range(0,lbda.size):
                permittivity_xx[lb,m]=(nxx+1j*kxx)**2 
                permittivity_yy[lb,m]=(nyy+1j*kyy)**2 
                permittivity_zz[lb,m]=(nzz+1j*kzz)**2                        
       
    return permittivity_xx,permittivity_yy,permittivity_zz