# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 03:20:25 2020

@author: Pink_Blossom
"""

def set_Output_Variable(idf, output, frequency = 'Monthly'):
    """
    Generate a new output:variable object

    Parameters
    ----------
    idf : eppy.modeleditor.IDF
        Eppy's IDF object.
    output : str
        output name (w.r.t. rdd data).
    frequency : str, optional
        Output resolution. The default is 'Monthly'.

    """
    # Add new IDF object
    obj = 'Output:Variable'
    idf.newidfobject(obj)
    my_object = idf.idfobjects[obj][-1]
    
    # Parameter
    setattr(my_object, 'Variable_Name', output)
    setattr(my_object, 'Reporting_Frequency', frequency)    
    
    