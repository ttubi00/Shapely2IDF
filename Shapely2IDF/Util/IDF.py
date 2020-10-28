# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 19:49:23 2020

@author: Pink_Blossom
"""

def kill_obj(idf, target, objname):
    """
    remove IDF object from EnergyPlus model based on 'Name' field

    Parameters
    ----------
    idf : eppy.modeleditor.IDF
        Eppy's IDF object.
    target : eppy.bunch_subclass.EpBunch
        target IDF object (w.r.t eppy).
    objname : str
        Object name to find.
    """
    idf.removeidfobject(target) if getattr(target, 'Name') == objname else 1+1
    
    
    
def is_DayType_Valid(DayType):
    """
    [W.R.T. Schedule:compact], Check user-input DayType whether valid

    Parameters
    ----------
    DayType : str
        user-input DayType (e.g. 'Sunday Holidays AllOtherDays', 'Saturday', 'Weekdays').

    Returns
    -------
    DayType : str or None (input Error)
        DayType after validation.

    """
    daytypes = ['Sunday Holidays AllOtherDays', 'Saturday', 'Weekdays']    

    try:
        daytypes.index(DayType)
    except ValueError:
        print('[schedule:compact] DayType %s is not invalid. The DayType will be ignored' %(DayType))
        return None
    else:
        return DayType
    

def DayTypes_validation(DayTypes):
    """
    [W.R.T. Schedule:compact], Check user-input DayTypeList whether valid    

    Parameters
    ----------
    DayTypes : list 
        user-input DayType list (e.g. ['Sunday Holidays AllOtherDays', 'Saturday', 'Weekdays']).

    Returns
    -------
    DayTypes : list
        DayType list after validation (e.g. [None, 'Saturday', 'Weekdays']).

    """
    DayTypes = [is_DayType_Valid(DayType) for DayType in DayTypes]    
    return DayTypes    