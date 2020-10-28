# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 17:38:53 2020

@author: Pink_Blossom
"""

from .Value import hr_2digit



def HourListZip_as_StrList(HourListZip):
    """
    [W.R.T. Schedule:compact] Conversion user-input HourLists to string Lists 

    Parameters
    ----------
    HourListZip : list
        user-input list of HourList.

    Returns
    -------
    list
        list of HourList after conversion.

    """
    return [[hr_2digit(hr) for hr in HourList] for HourList in HourListZip] 


def ValueList_as_StrList(ValueListZip):
    """
    [W.R.T. Schedule:compact] Conversion user-input ValueLists to string Lists     

    Parameters
    ----------
    ValueListZip : list
        user-input list of Value List.

    Returns
    -------
    list
        list of ValueListZip after conversion.

    """
    return [[str(val) for val in ValueList] for ValueList in ValueListZip] 

#%%
def is_twoLists_same(List1, List2):
    """
    check Whether the lengths of two Lists match

    Parameters
    ----------
    List1 : list
        first List.
    ValueListZip : list
        second List.

    Returns
    -------
    bool
        Whether Whether the lengths of two Lists match.

    """
    return True if len(List1) == len(List2) else False

#%%

def is_TwoListofLists(Llist1, Llist2):
    """
    check Whether the length of the internal list of two Lists of Lists matches

    Parameters
    ----------
    Llist1 : List of lists [N]
        1st List of lists.
    Llist2 : List of lists [N]
        2nd List of lists.

    Returns
    -------
    Boolean list [N]
        [bool(1), bool(2),...,bool(N)].

    """
    return [len(list1) == len(list2) for list1, list2 in zip(Llist1, Llist2)]


def __MonthList_validation(MonthList):
    """
    [W.R.T. Schedule:compact] input MonthList validation
    (e.g. [1,2,13] -> error (13 > 12))        

    Parameters
    ----------
    MonthList : List
        Month list (e.g. [1,2,12]).

    Returns
    -------
    MonthList : List or None (input error)
        e.g. ['Through: 1/31', 'Through: 2/28', 'Through: 12/31'].

    """
    
    Day_of_Month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] 
    prefix = 'Through: '
    
    if MonthList[-1] != 12:
        return None
    else:
        MonthList = [prefix + '%d/%d' %(Month, Day_of_Month[Month])  for Month in MonthList]
        return MonthList




