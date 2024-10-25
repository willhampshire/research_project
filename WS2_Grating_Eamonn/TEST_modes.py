# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 15:50:09 2023

@author: ph1pbx

Remade using OOP by Will Hampshire (whampshire1@sheffield.ac.uk)

"""

import math
import time
from typing import List
from pathlib import Path
import os
import sys
from math import pi
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from Functions.argument_angle import argument_angle
from Functions.RCWA_spectrum import RCWA_spectrum
from Functions.Plot_refractive_indices import Plot_refractive_indices
from Functions.epsilon2n import epsilon2n
from Functions.Lorentz_oscillator import Lorentz_oscillator

from chars import greek, phys # a list of useful unicode chars




# class definitions

class Pattern:
    """
    Takes period, filling factor, position, size, form, angle
    pos and size use [x, y] component
    """
    def __init__(self, period:float, filling:float, size:List[float], form:int=1, pos:List[float]=[0,0], angle:float=0):
        self.period = period
        self.filling = filling
        self.width:float = self.period * self.filling

        self.form = form
        self.pos = pos
        self.size = size
        self.angle = angle


class Material:
    """
    Specify the material properties
    args:
    name, dispersive
    kwargs:
    material_path, material_n_k, pattern, description
    """
    def __init__(self, name:str, dispersive:bool,
                 material_path:str=None, material_n_k:list=None,
                 pattern:Pattern=None, thickness:float=None, thickness_sub:float=None,
                 description:str=None):

        self.description = description
        self.name = name
        self.dispersive = dispersive
        self.material_path = material_path
        self.material_n_k = material_n_k
        self.thickness = thickness
        self.thickness_sub = thickness_sub



        # if non-dispersive (eg air) use [n,k], if dispersive, use string fname.
        if dispersive == True:
            assert self.material_n_k == None
            assert self.material_path != None
        if dispersive == False:
            assert self.material_n_k != None
            assert self.material_path == None

        # if pattern etched into material, assign self.pattern
        if pattern != None:
            self.pattern = pattern # e.g. period = self.pattern.period
        else:
            self.pattern = None


    def describe(self, extra:str=None):
        print(f"Material: {self.name}. "
              f"\nDescription: {self.description}\n{extra}\n")

    def make_layer(self, t:float, t_sub:float=None):
        """Create a copy of the Material instance to make an editable layer without editing the material.
        For t=t_sub, leave t_sub empty or = None

        Give args t, t_sub
        :returns: Material
        """
        if t_sub is None:
            t_sub = t
        return Material(
            name=self.name,
            dispersive=self.dispersive,
            material_path=self.material_path,
            material_n_k=self.material_n_k,
            pattern=self.pattern,
            description=self.description,
            thickness=t,
            thickness_sub=t_sub
        )


class Waveguide:
    """
    Stack the materials in layers to assemble the waveguide
    """
    def __init__(self):
        self._layers = []  # List to hold layers
        self._materials = [] # materials in order

    def add_layer(self, layer: Material):
        """Add a material layer to the waveguide. Appends to list."""
        self._layers.append(layer)
        # if material.name not in self._materials:
        #     self._materials.append(material)
        #     print(f"ADDED {material.name} {self._materials}")
        # else:
        #     print(f"{material.name} ALREADY IN {self._materials}"
        #           f" pos {self._materials.index(material.name)}")

    def write_material_order(self, materials:List[Material]):
        self._materials = materials

    def get_summary_name(self) -> str:
        names = []
        for _,layer in enumerate(self._layers):
            if layer.name != 'air':
                names.append(f'{layer.name}')

        return ', '.join(names)


    def describe(self):
        """Describe all layers in the waveguide."""
        print("\n\n--Waveguide Layers--")
        material_names = [mat.name for mat in self._materials]
        print(material_names)
        for i, layer in enumerate(self._layers):
            print(f"\nLayer {i + 1}:")
            mat_index = material_names.index(layer.name) + 1
            layer.describe(extra=f"Thickness: {layer.thickness}\nMaterial index: {mat_index}")


    def _materials_RCWA(self) -> List[str | List]:
        mats_temp = []
        for _,mat in enumerate(self._materials):
            if mat.dispersive == True:
                mats_temp.append(mat.material_path)
            if mat.dispersive == False:
                mats_temp.append(mat.material_n_k)
        return mats_temp

    def _layers_RCWA(self, sub:bool) -> List[List[float]]:
        layers_temp = []
        material_names = [mat.name for mat in self._materials]
        for i,layer in enumerate(self._layers):
            mat_index = material_names.index(layer.name) + 1 # return i 1-indexed
            try:
                layer.thickness_sub
            except:
                layer.thickness_sub = layer.thickness

            if sub==True:
                if layer.thickness_sub != None:
                    layers_temp.append([layer.thickness_sub,mat_index])

            if sub==False:
                layers_temp.append([layer.thickness, mat_index])
        return layers_temp

    def _pattern_RCWA(self) -> List:
        pattern_temp = []
        for i,layer in enumerate(self._layers):
            try:
                period = layer.pattern.period
                ff = layer.pattern.filling
                w = layer.pattern.width # period-w used to calc size_x when called
                form = layer.pattern.form
                pos = layer.pattern.pos
                size = layer.pattern.size
                angle = layer.pattern.angle

            except:
                # print(f"No pattens for layer {layer.name}")
                continue

            print(f"Patterned layer: {layer.name}, iloc in stack {i+1}, imat {i+1} (return {i}), form {form}")

            pattern_temp.append([i+1, i, form, pos, size, angle])
            print(f"Pattern: {pattern_temp}")
        return [pattern_temp[0]]

    # def _grating_thickness_remove(self):
    #     self._cache_layer_thickness = []
    #     for i, layer in enumerate(self._layers):
    #         try:
    #             assert layer.pattern != None # see if pattern exists for the layer
    #             #print(f"Layer thickness before: {layer.thickness:.2f}")
    #             self._cache_layer_thickness.append(layer.thickness)
    #             layer.thickness = 0
    #
    #             #print(f"Sub: Set thickness to {layer.thickness:.3f} for {layer.name}")
    #         except:
    #             continue

    # def _grating_thickness_replace(self):
    #     for i, layer in enumerate(self._layers):
    #         try:
    #             assert layer.pattern != None # see if pattern exists for the layer
    #             layer.thickness = self._cache_layer_thickness
    #
    #             #print(f"Sub: Set thickness to {layer.thickness:.3f} for {layer.name}")
    #         except:
    #             continue

    def export_RCWA_format(self, sub:bool, as_df:bool=None) -> List[List]:
        """
        Exports [material, layer, pattern] : List[List] for use with RCWA_spectrum function
        :param sub: sets pattern to [] and thickness of grating (patterned layer) to 0 + reverts
        :param as_df: exports material, layer data as DF for easy readability
        :return: [material, layer, pattern]
        """

        layer_RCWA = self._layers_RCWA(sub=sub)
        material_RCWA = self._materials_RCWA()
        pattern_RCWA = self._pattern_RCWA()


        if as_df == True:
            df = pd.concat([pd.Series(layer_RCWA, name='layer'), pd.Series(material_RCWA, name='material')], axis=1)
            return df

        return [material_RCWA, layer_RCWA, pattern_RCWA]



class SizeLimitException(Exception):
    def __init__(self, message="Size limit exceeded", exceeded=None):
        self.message = message
        self.exceeded = exceeded
        super().__init__(self.message)

    def __str__(self):
        if self.exceeded:
            return f"{self.message}. Out of bounds: {self.exceeded}"
        return self.message




# main function

def main(N:int):

    time_run = time.time()

    # %% Spectral range of the starting point
    N_lambda=N

    lbda_min = 1240 / 2.48
    lbda_max = 1240 / 1.54

    lbda = np.linspace(lbda_min/1000,lbda_max/1000,N_lambda)
    E=1.23987/lbda
    # %% Wave_vector
    # N_k=701
    N_k=N
    # k_scan=np.linspace(-6.7,6.7,N_k) #mu-1
    kmax=6.7
    k_scan=np.linspace(-kmax,kmax,N_k) #mu-1
    ky=0.000 #mu-1
    # %% Common parameters
    N_ord=7 #Choice of the number of orders taken into account during simulation, recommendation: 7 for 1D, 50 for 2D
    polar=2 #Polarization of incident wave: 1-> x, 2-> y, 3->L, 4->R, 5->s, 6->p, 7->45°, 8->-45°, 0-> All 6 polarizations (H,V,D,A,L,R) for the Stoke parameter


    # %% Materials definition(two ways: 1/ Location for a dispersive material; 2/[n,k] for a non-dispersive material
    #material=[]
    #material.append([1,0]) # superstrate air


    air = Material('air', dispersive=False,
                 material_n_k=[1,0],
                 description="Air.")
    air_layer = air.make_layer(t=0,t_sub=0)

    # 'Materials/SiO2_Horiba.txt'
    SiO2 = Material(f'SiO{phys.sub_2}', dispersive=False,
                   material_n_k=[1.46,0],
                   description=f"Silicon Dioxide substrate.")
    SiO2_layer = SiO2.make_layer(0.29)


    hBN = Material(f'hBN', dispersive=True,
                    material_path='Materials/hBN_Zotev.txt',
                    description=f"HBN.")
    hBN_layer_1 = hBN.make_layer(t=0.09, t_sub=0)
    hBN_layer_2 = hBN.make_layer(t=0.11, t_sub=0)
    hBN_layer_3 = hBN.make_layer(t=0.0, t_sub=0)


    Si = Material(f'Si', dispersive=True,
                   material_path='Materials/cSi_Green_2008.txt',
                   description=f"Silicon substrate.")
    Si_layer = Si.make_layer(2)


    Au = Material(f'Au', dispersive=True,
                   material_path='Materials/Au_Johnson.txt',
                   description=f"Gold layer.")
    Au_layer = Au.make_layer(0.150)


    WSe2 = Material(f'WSe{phys.sub_2}', dispersive=True,
                    material_path='Materials/WSe2_Zotev.txt',
                    # 'Materials/WSe2_Zotev.txt' 'Materials/WS2_Munkhbat2022.txt'
                    description=f"WSe{phys.sub_2}.")

    # WSe2_layer = WSe2.clone()
    WSe2_layer = WSe2.make_layer(t=0.001, t_sub=0)


    min_detail = 0.08  # um

    ax=0.425 # range .2 ~ .6
    FF=0.7 # ~ .8
    w=FF*ax

    # check wire and track detail level isnt smaller than 100nm
    if (w<0.1) or ((ax-w)<min_detail):
        #sys.exit(f"EXITING: w={w:.3f}, ax-w={ax-w:.3f} < {min_detail}")
        raise SizeLimitException(message="Cannot have track/wire feature <100nm.",
                                 exceeded=f"{w:.3f} or {ax-w:.3f} < {min_detail:.3f}")

    u = [ax, 0]
    v = [0, 0]

    pattern = Pattern(ax, FF, size=[ax-w,0])
    hBN_layer_2.pattern = pattern

    swg = Waveguide()
    swg.write_material_order([air,WSe2,hBN,hBN,Au,Si]) # simply the materials list, but instead with Material objects

    swg.add_layer(air_layer)
    swg.add_layer(hBN_layer_1)
    swg.add_layer(WSe2_layer)
    swg.add_layer(hBN_layer_2) # patterned
    swg.add_layer(hBN_layer_3) # zero thickness
    swg.add_layer(Au_layer)
    swg.add_layer(Si_layer)

    material_RCWA, layer_RCWA, pattern_RCWA = swg.export_RCWA_format(sub=False)
    swg.describe()

    material_RCWA_sub, layer_RCWA_sub, pattern_RCWA_sub = swg.export_RCWA_format(sub=True)

    #temp replace
    #debugging

    #layer_RCWA_sub = [[0, 1], [0, 2], [0, 3], [0, 4], [0.15, 5], [2, 6]]
    pattern_RCWA_sub = [[4, 1, 1, [0, 0], [0.1275, 0], 0]]
    # material_RCWA_sub = [[1, 0], 'Materials/WSe2_Zotev.txt', 'Materials/hBN_Zotev.txt', 'Materials/hBN_Zotev.txt',
    #                      'Materials/Au_Johnson.txt', 'Materials/cSi_Green_2008.txt']
    # material_RCWA = material_RCWA_sub
    pattern_RCWA = pattern_RCWA_sub


    print(swg.export_RCWA_format(sub=False, as_df=True))
    print(pd.Series(pattern_RCWA))
    print(pattern_RCWA)

    A=np.zeros((lbda.size,k_scan.size),dtype=float)
    R=np.zeros((lbda.size,k_scan.size),dtype=float)
    T=np.zeros((lbda.size,k_scan.size),dtype=float)
    A_sub=np.zeros((lbda.size,k_scan.size),dtype=float)
    R_sub=np.zeros((lbda.size,k_scan.size),dtype=float)
    T_sub=np.zeros((lbda.size,k_scan.size),dtype=float)
    for i_k in range(0, k_scan.size):
        kx = k_scan[i_k]
        k_inplan = math.sqrt(kx ** 2 + ky ** 2)
        ## Conic angle (in degrees)
        phi = argument_angle(kx, ky, k_inplan)
        ## Incident angles (in degrees)
        theta = np.arcsin(k_inplan / 2 / pi * lbda)
        theta = np.degrees(theta)
        remove_lambda = (abs(theta.imag) > 0).nonzero()
        theta[remove_lambda] = 0


        ## Run S4 simulation for each wavelength

        # print(f"--------------\nDEBUG\n{lbda,material_RCWA, layer_RCWA, pattern_RCWA,u,v,phi,theta,polar,N_ord}")

        lbda, R[:,i_k], T[:,i_k], A[:,i_k] = RCWA_spectrum(lbda,
                                                           material_RCWA, layer_RCWA, pattern_RCWA,
                                                           u,v,phi,theta,polar,N_ord)
        lbda, R_sub[:,i_k], T_sub[:,i_k], A_sub[:,i_k] = RCWA_spectrum(lbda,
                                                                       material_RCWA_sub, layer_RCWA_sub, pattern_RCWA_sub,
                                                                       u,v,phi,theta,polar,N_ord)
        # lbda,R_sub[:,i_k],T_sub[:,i_k],A_sub[:,i_k]=RCWA_spectrum(lbda,material,layer,pattern,u,v,phi,theta,8,N_ord)
        E=1.23984/lbda

        A[remove_lambda,i_k]=np.nan
        R[remove_lambda,i_k]=np.nan
        T[remove_lambda,i_k]=np.nan

        A_sub[remove_lambda,i_k]=np.nan
        R_sub[remove_lambda,i_k]=np.nan
        T_sub[remove_lambda,i_k]=np.nan

    # %%
    elapsed = time.time() - time_run
    print(f'\nElapsed time {elapsed:.1f}s')

    # %% Plot result
    signalR = (R - R_sub) / R_sub
    signalR = (signalR - np.min(signalR)) / (np.max(signalR) - np.min(signalR))
    # signalR=R

    signalA = (A - A_sub) / A_sub
    signalA = (signalA - np.min(signalA)) / (np.max(signalA) - np.min(signalA))
    signalA = A

    plt.rcParams['font.size'] = '16'


    # archaic legacy save name string
    #saving_name='t'+str("%.0f" % np.multiply(1e3,t))+'nm a='+str("%.0f" % np.multiply(1e3,ax))+'nm FF='+str("%.2f" % FF)

    details = (f"t={hBN_layer_2.thickness*1e3:.0f}nm "
               f"{greek.Lambda}={ax*1e3:.0f}nm "
               f"FF={FF:.2f}")

    Project_name = swg.get_summary_name()

    title_name = f"{Project_name}\n{details}"

    fig, axs = plt.subplots(1, 1, sharey=True, figsize=(7, 6), dpi=80)
    pcm = axs.pcolor(k_scan,1.240/lbda,signalR,cmap='viridis',clim=(0,1))
    axs.set(xlabel='k$_x$($\mu$m)',xlim=(-kmax,kmax),ylim=(1240/lbda_max, 1240/lbda_min), ylabel='Photon Energy(eV)',title=title_name)
    #axs.plot(k_scan,1.45*k_scan/k_scan,'m--') # reference line
    cbar =fig.colorbar(pcm,location='right')
    cbar.set_label('Reflectivity contrast')



    cwd = Path(os.getcwd())
    results_dir = cwd / "Results"
    results_dir.mkdir(exist_ok=True)

    dynamic_folder = results_dir / Project_name / (details + f' N={N}')
    dynamic_folder.mkdir(exist_ok=True, parents=True)

    images_folder = dynamic_folder / "images"
    data_folder = dynamic_folder / "data"
    images_folder.mkdir(exist_ok=True)
    data_folder.mkdir(exist_ok=True)



    R_data=np.column_stack([lbda, R])
    R_data=np.row_stack([np.concatenate([[np.nan],k_scan]), R_data])
    A_data=np.column_stack([lbda, A])
    A_data=np.row_stack([np.concatenate([[np.nan],k_scan]), A_data])
    T_data=np.column_stack([lbda, T])
    T_data=np.row_stack([np.concatenate([[np.nan],k_scan]), T_data])

    R_sub_data=np.column_stack([lbda, R_sub])
    R_sub_data=np.row_stack([np.concatenate([[np.nan],k_scan]), R_sub_data])
    A_sub_data=np.column_stack([lbda, A_sub])
    A_sub_data=np.row_stack([np.concatenate([[np.nan],k_scan]), A_sub_data])
    T_sub_data=np.column_stack([lbda, T_sub])
    T_sub_data=np.row_stack([np.concatenate([[np.nan],k_scan]), T_sub_data])

    np.savetxt(data_folder / (Project_name + ' - ' + details + "_R.csv"), R_data, delimiter=',')
    np.savetxt(data_folder / (Project_name + ' - ' + details + "_A.csv"), A_data, delimiter=',')
    np.savetxt(data_folder / (Project_name + ' - ' + details + "_T.csv"), T_data, delimiter=',')
    np.savetxt(data_folder / (Project_name + ' - ' + details + "_R_sub.csv"), R_sub_data, delimiter=',')
    np.savetxt(data_folder / (Project_name + ' - ' + details + "_A_sub.csv"), A_sub_data, delimiter=',')
    np.savetxt(data_folder / (Project_name + ' - ' + details + "_T_sub.csv"), T_sub_data, delimiter=',')

    #print(f"Data shape:\n{np.shape(T_sub_data)}")

    plt.savefig(images_folder / f"{Project_name} - {details}.png", dpi=150)
    plt.show()


# main entry point

main(N=50)



def test():
    """
    Testing and debugging function
    """
    test_material = Material(f"Test{phys.sub_3}", True, 'Materials/WS2_Munkhbat2022.txt',
                             pattern=Pattern(period=0.4, filling=0.8, size=(0.4 * (1 - 0.8))),
                             description="A test material.")

    # test_material.describe()
    print(test_material.pattern.period, test_material.pattern.filling, test_material.material_path)

    swg = Waveguide()
    layer1 = test_material.clone()
    layer1.thickness = 0.4
    swg.add_layer(layer1)

    layer2 = test_material.clone()
    layer2.thickness = 0.6
    swg.add_layer(layer2)

    print(f"Ensure thickness of matarial is None: '{test_material.thickness}'")

    swg.describe()
    print(swg.export_RCWA_format(sub=False, as_df=True).T)
    results = swg.export_RCWA_format(sub=False)

    material_RCWA, layer_RCWA, pattern_RCWA = results

#test()
