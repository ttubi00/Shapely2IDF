# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 00:11:45 2020

@author: Pink_Blossom

! Calculation of insulation thickness corresponding to input U values of exterior wall and roof floor

! Their constructions are assumed to be the medium type of ASHRAE HOF 2005.
! (Construction in 'Default IDF' in this module (Minimal.idf))

! For Roof & Floor, Apply the same insulation material as the wall (no insulation material in medium type)

! in calculations, effects of air-film will be ignored.

"""

''' resistance of materials have been pre-calculated'''

res = {}

# Opaque material
res['M01 100mm brick'] = 0.1016/0.89
res['G01a 19mm gypsum board'] = 0.019/0.16
res['M14a 100mm heavyweight concrete'] = 0.1016/1.95
res['F16 Acoustic tile'] = 0.0191/0.06



# Air gap
res['F04 Wall air space resistance'] = 0.15
res['F05 Ceiling air space resistance'] = 0.18


# insulation conductivity
ins_k = 0.03

def WallUvalue_material(WallU):
    R_input = 1/WallU
    R_other = res['M01 100mm brick'] + res['F04 Wall air space resistance'] + res['G01a 19mm gypsum board']
    R_ins =R_input-R_other
    d_ins = R_ins*ins_k
    return d_ins
    
    
def FloorUvalue_material(FloorU):    
    R_input = 1/FloorU
    R_other = res['F16 Acoustic tile'] + res['F05 Ceiling air space resistance'] + res['M14a 100mm heavyweight concrete']
    R_ins =R_input-R_other
    d_ins = R_ins*ins_k    
    return d_ins
    
    
def RoofUvalue_material(RoofU):        
    R_input = 1/RoofU
    R_other = res['M14a 100mm heavyweight concrete'] + res['F05 Ceiling air space resistance'] + res['F16 Acoustic tile']
    R_ins =R_input-R_other
    d_ins = R_ins*ins_k    
    return d_ins

    
    