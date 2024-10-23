# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 12:31:39 2023

@author: ph1pbx
"""


def Lorentz_oscillator(E,A,E0,gamma):
    
    eps= A/((E0**2-E**2)+gamma*E*1j)
            
    return eps