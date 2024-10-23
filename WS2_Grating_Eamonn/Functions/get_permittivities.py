# -*- coding: utf-8 -*-
"""
Created on Fri May 27 12:32:43 2022

@author: ph1pbx
"""

def get_permittivities(lbda,material):
    
    import numpy as np
    
    permittivity_r=np.zeros((lbda.size,len(material)),dtype=float)
    permittivity_i=np.zeros((lbda.size,len(material)),dtype=float)
    for m in range(0,len(material)):        
        if isinstance(material[m], str):        
            mat_refractive_index=np.genfromtxt(fname=material[m])
            check=np.diff(mat_refractive_index[:,0]) # check if the wavelength is decreasing
            if check[1]<0:
                mat_refractive_index=np.flipud(mat_refractive_index)
            n=np.interp(lbda,mat_refractive_index[:,0],mat_refractive_index[:,1])
            k=np.interp(lbda,mat_refractive_index[:,0],mat_refractive_index[:,2])
            permittivity_r[:,m]=n**2-k**2
            permittivity_i[:,m]=2*n*k
        else:
            n=material[m][0]
            k=material[m][1]
            for lb in range(0,lbda.size):
               permittivity_r[lb,m]=n**2-k**2
               permittivity_i[lb,m]=2*n*k                            
    permittivity=permittivity_r+1j*permittivity_i
        
    return permittivity