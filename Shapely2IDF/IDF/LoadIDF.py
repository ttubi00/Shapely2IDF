# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 15:44:25 2020

@author: Pink_Blossom
"""


from eppy.modeleditor import IDF
from copy import deepcopy

def gen_idf(idfname, iddname):
    """
    IDF file -> Eppy's IDF object 생성'

    Parameters
    ----------
    idfname : str
        IDF file name.
    iddname : str, optional
        IDD file name. The default is 'Energy+.idd'.

    Returns
    -------
    idf : eppy.modeleditor.IDF
        Eppy's IDF object.
    IDF_ : type
        eppy.modeleditor.IDF (deep-copied).

    """
    
    IDF_ = deepcopy(IDF) # Deepcopy
    IDF_.setiddname(iddname) # IDD registration
    idf = IDF_(idfname) # IDF registration                         
    return idf, IDF_