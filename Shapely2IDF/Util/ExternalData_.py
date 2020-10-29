# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 15:11:01 2020

@author: Pink_Blossom
"""
from __future__ import unicode_literals

from .List import __MonthList_validation
from .PythonData import DFcol2List, DFcol_filter 
from ..IDF.Schedule import schedule_compact_DayHour

import pandas as pd
import json
import pdb


def Gen_schedule_compact_ExternalForm(fname, sc_names):
    """
    Create Excel basic format for writing schedule compact information
    (User-form of External Data)

    Parameters
    ----------
    fname : str
        excel file name.
    sc_names : list
        object names of schedule compact.

    """

    df = pd.DataFrame(columns = ['Month', 'DayType', 'Hour', 'Value', 'TypeLimit'])
    writer = pd.ExcelWriter(fname, engine='xlsxwriter')
    [df.to_excel(writer, sheet_name = sc_name, index = False) for sc_name in sc_names]
    writer.save()


def MakeDict_schedule_compact_From_ExternalForm(fname):
    """    
    Create dictionary from schedule compact excel data

    Parameters
    ----------
    fname : TYPE
        DESCRIPTION.

    Raises
    ------
    Exception
        DESCRIPTION.

    Returns
    -------
    Sche_Dicts : list(dictionary)
        List of each schedule compact information.
    Sche_names : list(str)
        DESCRIPTION.
    TypeLimits : list(str)
        Typelimits list for each schedule compact.        

    """
    
    err_raise = lambda sheet_name: '[MakeDict_schedule_compact_From_ExternalForm] TypeLimit value of the schedule input data set is not the same. \n (sheetname: %s) %(sheet_name)'
    
    xlsx = pd.ExcelFile(fname)
    Sche_names = xlsx.sheet_names
    Sche_info = [xlsx.parse(Sche_name) for Sche_name in Sche_names]
    
    Sche_Dicts = []
    TypeLimits = []

    for idx, (sche_info, sche_name) in enumerate( zip(Sche_info, Sche_names) ):
        sche_dict = {}
        sche_dict['ObjName'] = sche_name
        
        
        # 단일 스케쥴 데이터에서 여러 TypeLimit 혼용여부 검사
        typelimit_unique = DFcol2List(sche_info, 'TypeLimit')
        if len(typelimit_unique) != 1:
            raise Exception(err_raise)
        else:
            TypeLimits.append(typelimit_unique[0])
        
        # 월 정보 (Schedule compact Field: For: 1/31,....)
        months_int = DFcol2List(sche_info, 'Month') # e.g. 1월, 3월, 12월 -> [1,3,12]
        months_str = __MonthList_validation(months_int) # e.g. [1,3,12] -> ['For: 1/31', 'For: 3/31', 'For: 12/31']

        for month_int, month_str in zip(months_int, months_str):
            
            # 데이터 세트에서 특정 month에 대응되는 sub-data 추출
            month_data = DFcol_filter(sche_info, 'Month', month_int)
            
            # DayType unque list 추출 (e.g. ['AllOtherDays', 'Weekdays'])
            DayTypes = DFcol2List(month_data, 'DayType')


            # DayType 별 데이터 검색 -> HourList & ValueList 추출 (List)
            HourListZip, ValueListZip = [], []

            for Dtype in DayTypes:
                # 특정 DayType를 만족하는 sub-data
                day_data = DFcol_filter(month_data, 'DayType', Dtype)
                
                HourListZip.append( DFcol2List(day_data, 'Hour', onlyunique = False))
                ValueListZip.append( DFcol2List(day_data, 'Value', onlyunique = False))                
            
            # 월별 스케쥴 정보 취합 ->     
            sche_dict[month_str] = schedule_compact_DayHour(DayTypes, HourListZip, ValueListZip)

        # Schedule compact 별 정보 취합    
        Sche_Dicts.append(sche_dict)

    return Sche_Dicts, Sche_names, TypeLimits


def Single_schedule_compact2JSON(Sche_Dict):
    """
    Output the schedule compact dictionary as a json file
    (Single schedule compact data)    

    Parameters
    ----------
    Sche_Dict : dictionary
        Schedule compact dictionary.

    Returns
    -------
    fname : str
        json file name.

    """

    objname = Sche_Dict['ObjName']
    fname = 'ScheduleCompact_%s.json' %(objname)
    with open(fname,'w') as f:
        json.dump(Sche_Dict,f)    
    return fname    

def Dict_schedule_compact2JSON(Sche_Dicts):
    """  
    Output the schedule compact dictionary as a json file
    (Multiple schedule compact data)    
    
    Parameters
    ----------
    Sche_Dicts : list
        List of Schedule compact dictionarys.

    Returns
    -------
        json files for each schedule compact data.
    """
    
    [Single_schedule_compact2JSON(Sche_Dict) for Sche_Dict in Sche_Dicts]



def get_location_epw(epwname):
    """
    Get location information from epw file
    (read epw's header -> extract location information)

    Parameters
    ----------
    epwname : str
        epw file name.

    Returns
    -------
    name : str
        location name.
    lat : str
        latitude.
    lon : str
        longitude.
    tzone : str
        time zone.
    elev : str
        elevation.

    """
    err_raise = '[get_location_epw] input epwfile name is invalid.'
    
    # Check whether epwfile name is invalid
    if epwname.endswith('.epw') == False:
        raise Exception(err_raise)
    
    # Parsing
    with open(epwname) as f:
        loc_data = f.readline()
        loc_data_split = loc_data.split(',')
        name = loc_data_split[1]
        lat = loc_data_split[6]
        lon = loc_data_split[7]
        tzone = loc_data_split[8]
        elev = loc_data_split[-1].split('\n')[0]
    return name, lat, lon, tzone, elev    
                    



def rdd_parse(rddfname):
    """
    rdd file (w.r.t. EnergyPlus available output list) parser

    Parameters
    ----------
    rddfname : str
        rdd file name.

    Returns
    -------
    outputs : list
        available outputs.

    """
    cnt = 0
    outputs = []
    
    sep1, sep2 = ',', ' ['
    
    with open(rddfname) as f:
        while 1:
            line = f.readline()
            
            if line == '': # End of file
                break
            
            if cnt > 1:
                line_split = line.split(sep1)
                output = line_split[-1]
                output = output.split(sep2)[0]                
                outputs.append(output)
            cnt += 1  
    return outputs
         

def rdd2Json(outputs, JSONfname, verbose = True):
    """
    Outputs from rdd data -> dictionary -> json file

    Parameters
    ----------
    outputs : list
        available outputs.
    JSONfname : TYPE
        json file name.
        
    Returns
    -------
    my_dict : dictionary
        outputs classified by output type.        

    """

    my_dict = {} 

    label = ''
    for out in outputs:
        new_label = out.split(' ')[0]
        if label != new_label:
            my_dict[new_label] = [out]
        else:
            my_dict[label].append(out)
        label = new_label    

    if verbose:
        print('')
        print('Available output types (EnergyPlus):')
        print(list(my_dict.keys()))
        print('')
        print('Total number of outputs (EnergyPlus)')
        print(len(outputs))
        print('')

    with open(JSONfname, 'w') as f:
        json.dump(my_dict, f)
    return my_dict    
    



        
    
    