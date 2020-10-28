# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 17:24:11 2020

@author: Pink_Blossom
"""



def DFcol2List(df, column_name, onlyunique = True):
    """
    Convert specific column of Pandas dataframe to list 

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        Pandas DataFrame.
    column_name : str
        Target column name.
    onlyunique : bool, optional
        Whether to extract unit list. The default is True.        

    Returns
    -------
    target : List
        Conversion result of target column of raw dataframe.
    """
    
    target_col = df[column_name]
    target = target_col.unique().tolist() if onlyunique == True else target_col.tolist()
    return target


def DFcol_filter(df, column_name, value):
    """
    Extracting Padnas sub-dataframe that satisfies a specific value

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        Pandas dataframe.
    column_name : str
        Target column name.
    value : anyvalue
        target value.

    Returns
    -------
    pandas.core.frame.DataFrame
        Pandas sub-dataframe.

    """
    
    # Error message
    err_raise = '[DFcol_filter] No data satisfying the search condition'

    # Extract sub-dataframe
    subframe = df[df[column_name] == value]
    
    # Raise error for empty sub-dataframe
    if len(subframe) ==0:
        raise Exception(err_raise)
    
    return subframe