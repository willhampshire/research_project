# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 16:52:57 2022

@author: ph1pbx
"""

def RCWA_fields(lbda,material,layer,pattern,u,v,phi,theta,polar,N_ord,zz,nx,ny):
    
    import numpy as np
    import S4 as S4
    from Functions.get_anisotropic_permittivities import get_anisotropic_permittivities
    from Functions.get_permittivities import get_permittivities
    from Functions.get_sp_Amplitude_Phase import get_sp_Amplitude_Phase
                
    permittivity_xx,permittivity_yy,permittivity_zz=get_anisotropic_permittivities(lbda,material)   # Set the materials permitivitties                                   
    # permittivity=get_permittivities(lbda,material)   # Set the materials permitivitties                                   
    # permittivity_xx=permittivity
    # permittivity_yy=permittivity
    # permittivity_zz=permittivity
    
    A_p,A_s,phase_p,phase_s=get_sp_Amplitude_Phase(polar,phi) #  Set the polarization   
        
    S = S4.New(Lattice = ((u[0],u[1]), (v[0],v[1])), NumBasis = N_ord)
              
    # set the materials
    for m in range(0,len(material)): 
        # S.AddMaterial(Name ='Mat'+str(m+1), Epsilon = permittivity[lb,m])
        S.SetMaterial(Name ='Mat'+str(m+1), Epsilon = (
                                                       (permittivity_xx[0,m], 0, 0),
                                                       (0, permittivity_yy[0,m], 0),
                                                       (0, 0, permittivity_zz[0,m])
                                                                                  ))
             
    # set the layers  
    for ly in range(0,len(layer)):
        S.AddLayer(Name ='Layer'+str(ly+1), Thickness = layer[ly][0], Material = 'Mat'+str(layer[ly][1])) 
            
    # set the pattern    
    if len(pattern)>0: # There is some pattern
        for p in range(0,len(pattern)):
            if pattern[p][2]==1: # grating
                S.SetRegionRectangle(Layer='Layer'+str(pattern[p][0]),Material='Mat'+str(pattern[p][1]), Center=(pattern[p][3][0],pattern[p][3][1]), Angle=0, Halfwidths=(pattern[p][4][0]/2,pattern[p][4][0]/2))
            elif pattern[p][2]==2: # circular
                S.SetRegionCircle(Layer='Layer'+str(pattern[p][0]),Material='Mat'+str(pattern[p][1]), Center=(pattern[p][3][0],pattern[p][3][1]), Halfwidths=pattern[p][4][0]/2)
            elif pattern[p][2]==3: # rectangular
                S.SetRegionRectangle(Layer='Layer'+str(pattern[p][0]),Material='Mat'+str(pattern[p][1]), Center=(pattern[p][3][0],pattern[p][3][1]), Angle=pattern[p][5], Halfwidths=(pattern[p][4][0]/2,pattern[p][4][0]/2))
            elif pattern[p][2]==4: # ellipse
                S.SetRegionEllipse(Layer='Layer'+str(pattern[p][0]),Material='Mat'+str(pattern[p][1]), Center=(pattern[p][3][0],pattern[p][3][1]), Angle=pattern[p][5], Halfwidths=(pattern[p][4][0]/2,pattern[p][4][0]/2))
            else:
                print("PATTERN DEFINITION: invalid pattern form")
            
    freq=1/lbda 
          
    S.SetExcitationPlanewave(IncidenceAngles=(theta,phi), sAmplitude=A_s*(np.exp(phase_s*1j)), pAmplitude=A_p*(np.exp(phase_p*1j)), Order=0) 
        
    S.SetFrequency(freq) 
        
    # E,H=S.GetFields(x, y, z)
    E,H=S.GetFieldsOnGrid(z=zz, NumSamples=(nx,ny), Format = 'Array')
        
    return E,H