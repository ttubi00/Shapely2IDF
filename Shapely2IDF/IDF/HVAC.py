# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 18:20:19 2020

@author: Pink_Blossom
"""

def HVAC_IdealLoadsAirSystem(idf, default_name = 'IdealLoadsAirSystem', thermostat_Name = 'thermo', HVACSche = 'HVACSche', 
                             HeatSche = 'Heating_set_point_sche', CoolSche = 'Cooling_set_point_sche', is_OA_use = True, OA_measure = 'Flow/Person', OA_method = 'Outdoor_Air_Flow_Rate_per_Person', OA_value = 6/3600):
    """
    IDF HVACTemplate:Zone:IdealLoadsAirSystem Object

    Parameters
    ----------
    idf : eppy.modeleditor.IDF
        Eppy's IDF object.
    default_name : str, optional
        Object name. The default is 'IdealLoadsAirSystem'.
    thermostat_Name : str, optional
        Thermostat Object name. The default is 'thermo'.
    HVACSche : str, optional
        HVAC Operating schedule Object name. The default is 'HVACSche'.
    HeatSche : str, optional
        Heating system Operating schedule Object name. The default is 'Heating_set_point_sche'.
    CoolSche : str, optional
        Cooling system Operating schedule Object nam. The default is 'Cooling_set_point_sche'.
    is_OA_use : Bool, optional
        Whether to introduce outside air. The default is True.
    OA_measure : str, optional
        Unit of air flow rate. The default is 'Flow/Person'.
    OA_method : str, optional
        Air flow rate measuring method. The default is 'Outdoor_Air_Flow_Rate_per_Person'.
    OA_value : float, optional
        Air flow rate value. The default is 6/3600.

    """

    # Error message
    err_raise1 = '[HVAC_IdealLoadsAirSystem] No thermal zone exists. Construct IDF zone before'
    err_raise2 = '[HVAC_IdealLoadsAirSystem] OA introduction measure %s is not invalid. Please check it' %(OA_measure)
    err_raise3 = '[HVAC_IdealLoadsAirSystem] OA introduction method %s is not invalid. Please check it' %(OA_method)  
    

    obj = 'HVACTemplate:Zone:IdealLoadsAirSystem'.upper()        
        
    # 측정 방법 (w.r.t Outdoor Air introduction)
    measure_type = 'Outdoor_Air_Method'    

    # 측정 단위 (w.r.t Outdoor Air introduction)
    Measure_methods = ['Flow/Person', 'Sum', 'Maximum', 'Flow/Area', 'Flow/Zone']

    # IDF field (w.r.t Outdoor Air introduction)
    Fields = [['Outdoor_Air_Flow_Rate_per_Person'],
              ['Outdoor_Air_Flow_Rate_per_Zone_Floor_Area',
               'Outdoor_Air_Flow_Rate_per_Zone'],
              ['Outdoor_Air_Flow_Rate_per_Person',
               'Outdoor_Air_Flow_Rate_per_Zone_Floor_Area',
               'Outdoor_Air_Flow_Rate_per_Zone'],
              ['Outdoor_Air_Flow_Rate_per_Zone_Floor_Area'],
              ['Outdoor_Air_Flow_Rate_per_Zone']]
    

    #%% Check zone existance
    Zones = idf.idfobjects['zone'.upper()]
    n_zone = len(Zones)
    
    if n_zone == 0: #  warning message & pass
        raise Exception(err_raise1)
    else:
        # Zone 탐색
        for idx in range(n_zone):
            zname = getattr(Zones[idx], 'Name')
            
            # 신규 object 생성
            idf.newidfobject(obj) 
            my_object = idf.idfobjects[obj][-1]  

            # 파라미터 매칭
            setattr(my_object, 'Zone_Name', zname)
            setattr(my_object, 'Template_Thermostat_Name', thermostat_Name)       # Thermostat object name 
            setattr(my_object, 'System_Availability_Schedule_Name', HVACSche)     # HVAC main schedule   
            setattr(my_object, 'Heating_Availability_Schedule_Name', HeatSche)    # HVAC heating schedule                
            setattr(my_object, 'Cooling_Availability_Schedule_Name', CoolSche)    # HVAC cooling schedule                            
            
            # 외기도입 고려 (Optional)
                      
            if is_OA_use:
                # Input validation 1: 측정 단위 적합성 (List에 입력정보 포함여부 검사)
                try:
                    measure_idx = Measure_methods.index(OA_measure)
                except ValueError:
                    raise Exception(err_raise2)
                else:
                    # Input validation 2: 측정단위와 관련 Field 연관성 (List에 입력정보 포함여부 검사)
                    try:
                        Fields[measure_idx].index(OA_method)
                    except ValueError:
                        raise Exception(err_raise3)
                    else:   # Input Validation Finish                                         
                        setattr(my_object, measure_type, OA_measure)
                        setattr(my_object, OA_method, OA_value)
                                


def HVAC_Thermostat(idf, default_name = 'thermo', Heat_setpoint_sche = 'Heat_setpoint_sche', Cool_setpoint_sche = 'Cool_setpoint_sche'):
    """
    IDF HVACTemplate:Thermostat Object

    Parameters
    ----------
    idf : eppy.modeleditor.IDF
        Eppy's IDF object.
    default_name : str, optional
        Object name. The default is 'thermo'.
    Heat_setpoint_sche : str, optional
        Heating setpoint schedule name. The default is 'Heat_setpoint_sche'.
    Cool_setpoint_sche : TYPE, optional
        Cooling setpoint schedule name. The default is 'Cool_setpoint_sche'.


    """

    obj = 'HVACTemplate:Thermostat'.upper()
    
    # Add new IDF object
    idf.newidfobject(obj) 
    my_object = idf.idfobjects[obj][-1]  

    # Thermostat parameter
    setattr(my_object, 'Name', default_name)
    setattr(my_object, 'Heating_Setpoint_Schedule_Name', Heat_setpoint_sche)           
    setattr(my_object, 'Cooling_Setpoint_Schedule_Name', Cool_setpoint_sche) 
    
    

def set_Sim_control(idf, zone_sizing = False, system_sizing = False, plant_sizing = False, sizing_period = False, epw_period = True):
    obj = 'SimulationControl'.upper()
    idfobj = idf.idfobjects[obj][0]
    
    Zone_sizing = 'Yes' if zone_sizing == True else 'No'
    System_sizing = 'Yes' if system_sizing == True else 'No'
    Plant_sizing = 'Yes' if plant_sizing == True else 'No'
    Sizing_period = 'Yes' if sizing_period == True else 'No'
    EPW_period = 'Yes' if epw_period == True else 'No'

    setattr(idfobj, 'Do_Zone_Sizing_Calculation', Zone_sizing)
    setattr(idfobj, 'Do_System_Sizing_Calculation', System_sizing)
    setattr(idfobj, 'Do_Plant_Sizing_Calculation', Plant_sizing)
    setattr(idfobj, 'Run_Simulation_for_Sizing_Periods', Sizing_period)
    setattr(idfobj, 'Run_Simulation_for_Weather_File_Run_Periods', EPW_period)     