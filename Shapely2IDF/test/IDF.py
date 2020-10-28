# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 15:11:01 2020

@author: Pink_Blossom
"""
from __future__ import unicode_literals
import pandas as pd
from ..Util.List import __MonthList_validation



def Gen_schedule_compact_ExternalForm(fname, sc_names):

    df = pd.DataFrame(columns = ['Month', 'DayType', 'Hour', 'Value', 'TypeLimit'])
    writer = pd.ExcelWriter(fname, engine='xlsxwriter')
    [df.to_excel(writer, sheet_name = sc_name, index = False) for sc_name in sc_names]
    writer.save()



# def Get_schedule_compact_From_ExternalForm(fname):

#     # Load excelfile
#     xlsx = pd.ExcelFile(fname2)

#     # Get schedule names from sheet names
#     sche_names = xlsx.sheet_names
    
#     # Number of schedules
#     n_sche = len(sche_names)
    
#     # Get schedule informations
#     Sches = [xlsx.parse(sche_name) for sche_name in sche_names]
    
#     # Convert the informations to Dictionary
#     Dicts = [{}]*n_sche # empty dictionaries

#     ####
#     MonthList = __MonthList_validation(MonthList) # integer list -> str list
    
    
    


if __name__ == '__main__':
    fname = 'Schedule_compact.xlsx'
    schedule_compact_names = ['Occupancy', 'Activity', 'Lighting', 'Infiltration', 'HVACSche', 
                              'HeatSche', 'CoolSche', 'Heat_setpoint_sche', 'Cool_setpoint_sche']
    
    Gen_schedule_compact_ExternalForm(fname, schedule_compact_names)
    
    fname2 = 'Schedule_compact2.xlsx'
    xlsx = pd.ExcelFile(fname2)
    
    sc_names = xlsx.sheet_names
    
    DFs = [xlsx.parse(sc_name) for sc_name in sc_names]
    print(sc_names)