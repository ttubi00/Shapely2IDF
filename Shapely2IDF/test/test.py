# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 15:11:01 2020

@author: Pink_Blossom
"""
from __future__ import unicode_literals
import pandas as pd

def Gen_schedule_compact_ExternalForm(fname, sc_names):

    df = pd.DataFrame(columns = ['Month', 'DayType', 'Hour', 'Value', 'TypeLimit'])
    writer = pd.ExcelWriter(fname, engine='xlsxwriter')
    [df.to_excel(writer, sheet_name = sc_name, index = False) for sc_name in sc_names]
    writer.save()


if __name__ == '__main__':
    fname = 'Schedule_compact.xlsx'
    schedule_compact_names = ['Occupancy', 'Activity', 'Lighting', 'Infiltration', 'HVACSche', 
                              'HeatSche', 'CoolSche', 'Heat_setpoint_sche', 'Cool_setpoint_sche']
    
    Gen_schedule_compact_ExternalForm(fname, schedule_compact_names)