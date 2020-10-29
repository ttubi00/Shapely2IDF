# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 18:19:47 2020

@author: Pink_Blossom
"""

from ..Util.List import is_twoLists_same, is_TwoListofLists, __MonthList_validation
from ..Util.Value import hr_2digit
from ..Util.IDF import kill_obj
from copy import deepcopy
import json
import pdb

#%%
def get_schedule_compact(idf, objname):
    """
    [W.R.T. IDF], Search Schedule:compact object correspond to user-input object name

    Parameters
    ----------
    idf : eppy.modeleditor.IDF
        Eppy's IDF object.
    objname : str
        "Object name" of IDF Schedule:compact .

    Returns
    -------
    eppy.bunch_subclass.EpBunch
        IDF schedule:compact object w.r.t. input Object name.

    """
    
    obj = 'schedule:compact'.upper()
    idfobjs = idf.idfobjects[obj]
    objnames = [getattr(idfobj, 'Name') for idfobj in idfobjs]

    try:
        return idfobjs[objnames.index(objname)]
    except ValueError:
        return None

#%%
def sche_compact_field(idfobj, field_idx, str_value):
    """
    IDF schedule compact field 매칭

    Parameters
    ----------
    idfobj : eppy.bunch_subclass.EpBunch
        Eppy's schedule compact object.
    field_idx : int
        field index.
    str_value : str
        field value.

    Returns
    -------
    int
        Next field index.

    """
    setattr(idfobj, 'Field_%d' %(field_idx), str_value) 
    return field_idx+1     


#%%
def init_schedule_compact(idf, objname, TypeLimit = 'Fraction'):
    # Add new IDF object
    obj = 'schedule:compact'.upper()
    idf.newidfobject(obj) 
    my_object = idf.idfobjects[obj][-1]

    # Parameter
    setattr(my_object, 'Name', objname)
    setattr(my_object, 'Schedule_Type_Limits_Name', TypeLimit)
    
    return my_object


def WriteField_Monthly_schedule_compact(target, Month, DayInfo, field_idx):  

    #%% 
    field_idx = sche_compact_field(target, field_idx, Month)
    
    for DayType, HrVals in zip(DayInfo.keys(), DayInfo.values()):
        field_idx = sche_compact_field(target, field_idx, DayType)
        for HrVal in HrVals:
            Hour, Value = HrVal[0], HrVal[1]

            field_idx = sche_compact_field(target, field_idx, Hour)        
            field_idx = sche_compact_field(target, field_idx, Value)
    
    return field_idx  


#%%
def schedule_compact_DayHour(DayTypes = None, HourListZip = None, ValueListZip = None):

    # empty input -> set default input (else: use user-input)

    DayTypes = ['Sunday Holidays AllOtherDays', 'Saturday', 'Weekdays'] if DayTypes == None else DayTypes
    HourListZip = [ [24] ] if HourListZip == None else HourListZip # default: Until: 24:00
    ValueListZip = [ [1] ] if ValueListZip == None else ValueListZip # default: 1   

    # user-input validation (compare list lengths)

    isSame_DayTypes_HourListZip = is_twoLists_same(DayTypes, HourListZip) 
    isSame_DayTypes_ValueListZip = is_twoLists_same(DayTypes, ValueListZip)
    isSame_Hourlist_ValueListZip = is_TwoListofLists(HourListZip, ValueListZip) # [True, True, False]


    # Error message
    err_raise1 = '[schedule_compact_DayHour] DayTypes length & HourlistZip length not equal. Please check input variables'
    err_raise2 = '[schedule_compact_DayHour] DayTypes length & ValueListZip length not equal. Please check input variables'
    err_raise3 = '[schedule_compact_DayHour] HourListZip length & ValueListZip length not equal. Please check input variables'

    # pdb.set_trace()
    
    if isSame_DayTypes_HourListZip == False:
        raise Exception(err_raise1)
        
    elif isSame_DayTypes_ValueListZip == False:
        raise Exception(err_raise2)

    elif sum(isSame_Hourlist_ValueListZip) < len(isSame_Hourlist_ValueListZip): # e.g. sum[True, False]) = 1; len[True, False]) = 2
        raise Exception(err_raise3)
        
    # gen schedule:compact information as dictionary
    prefix1 = 'For: '
    prefix2 = 'Until: '
    
    sche_compact_DayHour = {}
    
    # pdb.set_trace()
    
    for DayType, HourList, ValueList in zip(DayTypes, HourListZip, ValueListZip):
        sche_compact_DayHour[prefix1 + DayType] = [(prefix2 + hr_2digit(hr) + ':00', str(value)) for hr, value in zip(HourList, ValueList)]
    
    return sche_compact_DayHour

#%%
def schedule_compact_Month(MonthList = [12], sche_compact_DayHourList = None, objname = 'dummy', isjson = True):

    # Error message
    err_raise1 = '[schedule_compact_Month] invalid input (input: MonthList)'
    err_raise2 = '[schedule_compact_Month] empty input (input: sche_compact_DayHourList)'

    # MonthList validation
    MonthList = __MonthList_validation(MonthList) # integer list -> str list

    # Raise Error for invalid user-input
    if MonthList == None:
        raise Exception(err_raise1)        
    
    if sche_compact_DayHourList == None:
        raise Exception(err_raise2)
    
    # Monthly meta data for building "schedule_compact" object
    sche_compact_Month = {'ObjName': objname}
    
    for Month, sche_compact_DayHour in zip(MonthList, sche_compact_DayHourList):
        sche_compact_Month[Month] = sche_compact_DayHour
    
    # Dump schedule compact information as JSON file
    if isjson:
        with open('ScheduleCompact_%s.json' %(objname),'w') as f:
            json.dump(sche_compact_Month,f)
    
    return sche_compact_Month  


def build_schedule_compact_dict(idf, sche_compact_Month = None, TypeLimit ='Fraction'):
    # Error message
    err_raise = '[build_schedule_compact_dict] empty input (input: schedule_compact_info)'
    
    # no schedule information input -> raise error
    if sche_compact_Month == None: 
        raise Exception(err_raise)

    # copy user-input (deepcopy)
    sc = deepcopy(sche_compact_Month)
    
    # remove exist schedule:compact object w.r.t user-input object name
    objname = sc['ObjName'] # read object name fron dictionary
    target = get_schedule_compact(idf, objname)
    kill_obj(idf, target, objname) if target != None else 1+1

    # remain only schedule:compact information
    del sc['ObjName']    

    # gen new schedule:compact object
    target = init_schedule_compact(idf, objname, TypeLimit)
    
    # write user-input to IDF's schedule:compact object
    
    field_idx = 1 # first Schedule:compact field index (sequencial update)

    
    for Month, DayInfo in zip( sc.keys(), sc.values() ):
        field_idx = WriteField_Monthly_schedule_compact(target, Month, DayInfo, field_idx)