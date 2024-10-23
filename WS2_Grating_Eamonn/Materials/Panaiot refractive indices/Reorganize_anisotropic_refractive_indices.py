# -*- coding: utf-8 -*-
"""
Created on Mon May 30 17:24:48 2022

@author: ph1pbx
"""

import numpy as np

Material_name='NiPS3'

data=np.genfromtxt(Material_name+'_exported_xy_n.txt')
lbda=data[:,0]
n_xy=data[:,1]

data=np.genfromtxt(Material_name+'_exported_xy_k.txt')
k_xy=data[:,1]

data=np.genfromtxt(Material_name+'_exported_zz_n.txt')
n_zz=data[:,1]

data=np.genfromtxt(Material_name+'_exported_zz_k.txt')
k_zz=data[:,1]

ref_ind=lbda
ref_ind=np.row_stack([ref_ind, n_xy])
ref_ind=np.row_stack([ref_ind, k_xy])
ref_ind=np.row_stack([ref_ind, n_xy])
ref_ind=np.row_stack([ref_ind, k_xy])
ref_ind=np.row_stack([ref_ind, n_zz])
ref_ind=np.row_stack([ref_ind, k_zz])

ref_ind=ref_ind.conj().transpose()

np.savetxt(Material_name+"_Zotev.txt", ref_ind)


