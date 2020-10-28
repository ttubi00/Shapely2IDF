# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 15:39:45 2020

@author: Pink_Blossom
"""

from Shapely2IDF.Material import __path__
import os
from shutil import copy

def get_minimalIDF(mypath):
    cpath = __path__[0]
    idfname = os.path.join(cpath, 'Minimal.idf')
    iddname = os.path.join(cpath, 'Energy+.idd')

    copy(idfname, os.path.join(mypath, 'Minimal.idf'))
    copy(iddname, os.path.join(mypath, 'Energy+.idd'))    
    return 'Minimal.idf', 'Energy+.idd'
    



 