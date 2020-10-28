# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 01:24:16 2020

@author: Pink_Blossom
"""

def SimpleGlazing_all(idf, Uvalue = 3, SHGC = 0.5):
    """
    Applying U value and SHGC collectively to all fenestration
    (WindowMaterial:SimpleGlazingSystem)

    Parameters
    ----------
    idf : eppy.modeleditor.IDF
        Eppy's IDF object.
    Uvalue : TYPE, optional
        DESCRIPTION. The default is 3.
    SHGC : TYPE, optional
        DESCRIPTION. The default is 0.5.

    """
    obj = 'WindowMaterial:SimpleGlazingSystem'.upper()
    idfobjs = idf.idfobjects[obj]
    
    [setattr(idfobj, 'UFactor', Uvalue) for idfobj in idfobjs]
    [setattr(idfobj, 'Solar_Heat_Gain_Coefficient', SHGC) for idfobj in idfobjs]    
    
    
def SimpleGlazing_each(idf, objname = 'fenestration', Uvalue = 3, SHGC = 0.5):
    """    
    Edit U value and SHGC of specific fenestration

    Parameters
    ----------
    idf : eppy.modeleditor.IDF
        Eppy's IDF object.
    objname : str, optional
        Specific IDF object name. The default is 'fenestration'.
    Uvalue : float, optional
        Fenestration U-value. The default is 3.
    SHGC : float, optional
        Fenestration SHGC. The default is 0.5.

    Raises
    ------
    Exception
        Invalid input IDF object name.

    """
    err_raise = '[SimpleGlazing_each] invalid IDF object name (objname: %s)' %(objname)

    obj = 'WindowMaterial:SimpleGlazingSystem'.upper()
    idfobjs = idf.idfobjects[obj]

    # Get all IDF object names
    obj_names = [idfobj.Name for idfobj in idfobjs]
    
    # Find target IDF object (using object name equality)
    try:
        target = obj_names.index(objname) # Find object index w.r.t objname
    except ValueError:
        raise Exception(err_raise) # invalid input (objname)

    # Edit properties
    setattr(target, 'UFactor', Uvalue)
    setattr(target, 'Solar_Heat_Gain_Coefficient', SHGC)
    
    
    