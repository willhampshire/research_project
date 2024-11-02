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

    def __str__(self):
        return (f"Pattern(p={self.period:.3f}, ff={self.filling:.3f}, "
                f"w={self.width:.3f}, form={self.form:.3f})")


class Material:
    """
    Specify the material properties
    :param name :str - give a name
    :param dispersive :bool - when False, provide material_n_k, when True, provide fpath to material profile
    :param material_path :str
    :param material_n_k :List[float]
    :param description :str
    :param pattern :Pattern - define on call or assign later
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
            disp = [dispersion for dispersion in [layer.material_n_k, layer.material_path] if dispersion is not None]
            layer.describe(extra=f"Thickness/sub: {layer.thickness}/{layer.thickness_sub}\n"
                                 f"Material index: {mat_index}\nDispersion: {disp[0]}")

    def summary_txt(self) -> str:
        summary = ""
        details = [
            'name',
            'dispersive',
            'material_path',
            'material_n_k',
            'pattern',
            'description',
            'thickness',
            'thickness_sub'
        ]
        for i,layer in enumerate(self._layers):
            summary += f"-- Layer {i+1} --\n"
            for detail in details:
                value = getattr(layer, detail)  # Get the value of the attribute
                summary += f"{detail}: {value}\n"  # Append to summary string
            summary += '\n'

        return summary

    def summary_csv(self):
        # Initialize an empty list to hold records (layers)
        records = []
        details = [
            'name',
            'dispersive',
            'material_path',
            'material_n_k',
            'pattern',
            'description',
            'thickness',
            'thickness_sub'
        ]

        # Loop through each layer and create a record for it
        for layer in self._layers:
            record = {}
            for detail in details:
                record[detail] = getattr(layer, detail, None)
            records.append(record)

        # Create DataFrame from the list of records
        summary = pd.DataFrame(records, columns=details)

        return summary


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

            # print(f"Patterned layer: {layer.name}, iloc in stack {i+1}, imat {i+1} (return {i}), form {form}")

            pattern_temp.append([i+1, i, form, pos, size, angle])
            # print(f"Pattern: {pattern_temp}")
        return pattern_temp

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


# define timing decorator
def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{elapsed_time:.1f} seconds elapsed - {func.__name__}")
        return result
    return wrapper




# main function
@time_it
def run_simulation(N:int, period:float, thickness:float, filling:float,
                   experiment_suf:str=None):
    """
    Main sim function.
    :param N simulation resolution
    :param period :float
    :param thickness_pattern :float
    :param filling :float
    :return: None
    """

    lbda_min = 1240 / 2.2 # y limits
    lbda_max = 1240 / 1.2

    lbda = np.linspace(lbda_min/1000,lbda_max/1000,N)
    # E=1.23987/lbda
    # Wave_vector
    # N_k=701
    N_k=N
    # k_scan=np.linspace(-6.7,6.7,N_k) #mu-1
    kmax=5
    k_scan=np.linspace(-kmax,kmax,N_k) #mu-1
    ky=0.000 #mu-1
    N_ord=7 #Choice of the number of orders taken into account during simulation, recommendation: 7 for 1D, 50 for 2D
    polar=2 #Polarization of incident wave: 1-> x, 2-> y, 3->L, 4->R, 5->s, 6->p, 7->45°, 8->-45°, 0-> All 6 polarizations (H,V,D,A,L,R) for the Stoke parameter


    # Materials definition, 2 ways:
    # 1 - Location for a dispersive material;
    # 2 - [n,k] for a non-dispersive material

    air = Material('air', dispersive=False,
                 material_n_k=[1,0],
                 description="Air.")

    # 'Materials/SiO2_Horiba.txt'
    SiO2 = Material(f'SiO{phys.sub_2}', dispersive=False,
                   material_n_k=[1.46,0],
                   description=f"Silicon Dioxide substrate.")

    hBN = Material(f'hBN', dispersive=True,
                    material_path='Materials/hBN_Zotev.txt',
                    description=f"HBN.")

    Si = Material(f'Si', dispersive=True,
                   material_path='Materials/cSi_Green_2008.txt',
                   description=f"Silicon substrate.")

    Au = Material(f'Au', dispersive=True,
                   material_path='Materials/Au_Johnson.txt',
                   description=f"Gold layer.")

    WS2 = Material(f'WS{phys.sub_2}', dispersive=True,
                   material_path='Materials/WS2_Munkhbat2022.txt',
                   # 'Materials/WSe2_Zotev.txt' 'Materials/WS2_Munkhbat2022.txt'
                   description=f"TMD layer, WS{phys.sub_2}.")


    min_detail = 100/1000  # 100 nm

    ax=period # range .2 ~ .6
    FF=filling # ~ .8
    w=FF*ax

    u = [ax, 0]
    v = [0, 0]

    # check wire and track detail level isnt smaller than 100nm
    if (w<0.1) or ((ax-w)<min_detail):
        #sys.exit(f"EXITING: w={w:.3f}, ax-w={ax-w:.3f} < {min_detail}")
        raise SizeLimitException(message="Cannot have track/wire feature <100nm.",
                                 exceeded=f"{w:.3f} or {ax-w:.3f} < {min_detail:.3f}")


    # make the layers
    air_layer = air.make_layer(t=0, t_sub=0)
    WS2_layer = WS2.make_layer(t=thickness, t_sub=0)
    Si_layer = Si.make_layer(2)
    # Au_layer = Au.make_layer(0.150)
    SiO2_layer = SiO2.make_layer(0.29)

    # pattern the grating layer
    WS2_layer.pattern = Pattern(ax, FF, size=[ax-w,0])

    swg = Waveguide() # make Waveguide object
    swg.write_material_order([air,WS2,SiO2,Si]) # simply the materials list, but instead with Material objects
    # could be made redundant by adding automatically when adding the layers, however easier to set order for testing
    # will throw error if layer used but its material is not added here

    swg.add_layer(air_layer)
    swg.add_layer(WS2_layer)
    swg.add_layer(SiO2_layer)
    #swg.add_layer(Au_layer)
    swg.add_layer(Si_layer)

    material_RCWA, layer_RCWA, pattern_RCWA = swg.export_RCWA_format(sub=False)
    # swg.describe()

    material_RCWA_sub, layer_RCWA_sub, pattern_RCWA_sub = swg.export_RCWA_format(sub=True)


    # print(swg.export_RCWA_format(sub=False, as_df=True))
    # print(pd.Series(pattern_RCWA))
    # print(pattern_RCWA)

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
        # E=1.23984/lbda

        A[remove_lambda,i_k]=np.nan
        R[remove_lambda,i_k]=np.nan
        T[remove_lambda,i_k]=np.nan

        A_sub[remove_lambda,i_k]=np.nan
        R_sub[remove_lambda,i_k]=np.nan
        T_sub[remove_lambda,i_k]=np.nan


    signalR = (R - R_sub) / R_sub
    signalR = (signalR - np.min(signalR)) / (np.max(signalR) - np.min(signalR))
    # signalR=R

    signalA = (A - A_sub) / A_sub
    signalA = (signalA - np.min(signalA)) / (np.max(signalA) - np.min(signalA))
    # signalA = A




    # legacy save name string
    #saving_name='t'+str("%.0f" % np.multiply(1e3,t))+'nm a='+str("%.0f" % np.multiply(1e3,ax))+'nm FF='+str("%.2f" % FF)

    # change t=layer.thickness variable when running other sims
    details = (f"t={WS2_layer.thickness*1e3:.1f}nm "
               f"{greek.Lambda}={ax*1e3:.0f}nm "
               f"FF={FF:.2f}")

    project_name = f'{swg.get_summary_name()} {experiment_suf}'
    # project_name = 'feature testing'

    title_name = f"{project_name}\n{details}"
    plt.rcParams['font.size'] = '16'

    fig, axs = plt.subplots(1, 1, sharey=True, figsize=(7, 6), dpi=80)
    pcm = axs.pcolor(k_scan,1.240/lbda,signalR,cmap='viridis',clim=(0,1))
    axs.set(xlabel=f'k$_x$ [{greek.mu}m]',xlim=(-kmax,kmax),ylim=(1240/lbda_max, 1240/lbda_min), ylabel='Photon Energy [eV]',title=title_name)
    # y_eV = 1.45    # reference line at 1.45eV
    # axs.plot(k_scan,y_eV*k_scan/k_scan,'m--') # reference line at 1.45eV
    cbar =fig.colorbar(pcm,location='right')
    cbar.set_label('Reflectivity contrast')
    plt.minorticks_on()

    cwd = Path(os.getcwd())
    results_dir = cwd / "Results"
    results_dir.mkdir(exist_ok=True)

    dynamic_folder = results_dir / project_name / (details + f' N={N}')
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


    np.savetxt(data_folder / (project_name + ' - ' + details + "_R.csv"), R_data, delimiter=',')
    np.savetxt(data_folder / (project_name + ' - ' + details + "_A.csv"), A_data, delimiter=',')
    np.savetxt(data_folder / (project_name + ' - ' + details + "_T.csv"), T_data, delimiter=',')
    np.savetxt(data_folder / (project_name + ' - ' + details + "_R_sub.csv"), R_sub_data, delimiter=',')
    np.savetxt(data_folder / (project_name + ' - ' + details + "_A_sub.csv"), A_sub_data, delimiter=',')
    np.savetxt(data_folder / (project_name + ' - ' + details + "_T_sub.csv"), T_sub_data, delimiter=',')

    info_file_path = data_folder / f"INFO {project_name} - {details}.txt"
    info_csv_file_path = data_folder / f"INFO {project_name} - {details}.csv"
    with open(info_file_path, 'w') as f:
        f.write(swg.summary_txt())

    swg.summary_csv().to_csv(info_csv_file_path, index=False)

    #print(f"Data shape:\n{np.shape(T_sub_data)}")

    plt.savefig(images_folder / f"{project_name} - {details}.png", dpi=150)
    plt.show()


    # print("*** SUMMARY ***")
    # print(swg.summary_txt())


def range_in(start:float, stop:float, step:float) -> List[float]:
    """
    Inclusive range generator
    Output rounded to 6dp
    :return: np.array
    """
    n_points = round(((stop-start)/step),0) +1
    linspace = list(np.linspace(start, stop, int(n_points)))
    return [round(num, 6) for num in linspace]

# main entry point
@time_it
def main() -> None:
    iterations = 0

    periods = [0.2, 0.4, 0.6]
    thicknesses = [0.02, 0.06, 0.1]
    filling = [0.5, 0.7, 0.9]

    # periods = range_in(0.25, 0.6, 0.05)
    # thicknesses = range_in(0.02, 0.1, (5/1000))
    # filling = range_in(0.5, 0.9, 0.1)

    num_loops = len(periods)*len(thicknesses)*len(filling)
    print(f"Estimated time for {num_loops:.0f} loops, 10s * {num_loops:.0f} = {10*num_loops/60:.1f}mins for N=75.")
    print(f"PERIODS {periods}\nTHICKNESSES {thicknesses}\nFILLINGS {filling}")
    time.sleep(1)

    for ax in periods:
        for t in thicknesses:
            for ff in filling:
                iterations += 1
                try:
                    run_simulation(75, period=ax, thickness=t, filling=ff, experiment_suf='3')
                except SizeLimitException as e:
                    print(e.message)
                    continue # skip current iteration if features <100nm
                finally:
                    print(f"Iteration {iterations} complete - p={ax:.3f} t={t:.3f} ff={ff:.2f}")


main()

# print(range_in(1, 5, 1))

# def test():
#     """
#     Testing and debugging function
#     """
#     test_material = Material(f"Test{phys.sub_3}", True, 'Materials/WS2_Munkhbat2022.txt',
#                              pattern=Pattern(period=0.4, filling=0.8, size=(0.4 * (1 - 0.8))),
#                              description="A test material.")
#
#     # test_material.describe()
#     print(test_material.pattern.period, test_material.pattern.filling, test_material.material_path)
#
#     swg = Waveguide()
#     layer1 = test_material.clone()
#     layer1.thickness = 0.4
#     swg.add_layer(layer1)
#
#     layer2 = test_material.clone()
#     layer2.thickness = 0.6
#     swg.add_layer(layer2)
#
#     print(f"Ensure thickness of matarial is None: '{test_material.thickness}'")
#
#     swg.describe()
#     print(swg.export_RCWA_format(sub=False, as_df=True).T)
#     results = swg.export_RCWA_format(sub=False)
#
#     material_RCWA, layer_RCWA, pattern_RCWA = results
#
# #test()
