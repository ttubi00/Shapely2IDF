# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 00:54:50 2020

@author: Pink_Blossom
"""


def find_insulation_obj(idf, ins_name):
    obj = 'material'.upper()
    idfobjs = idf.idfobjects[obj]
    material_names = [idfobj.Name for idfobj in idfobjs]
    
    # Find target IDF object (using object name equality)
    try:
        target_idx = material_names.index(ins_name)
    except ValueError:
        return False # Temporary results
    else:
        target = idfobjs[target_idx]
        return target
        
    

def insulation_thickness(idf, thickness, ins_name = 'I02 50mm insulation board'):
    err_raise = '[insulation_thickness] invalid insulation name (ins_name: %s)' %(ins_name)

    # Find target IDF object
    target = find_insulation_obj(idf, ins_name)

    # User-input validation
    if target == False:
        raise Exception(err_raise) # invalid input (ins_name)
        
    # Edit insulation thickness
    setattr(target, 'Thickness', thickness)

    
        
        
        

    
    
