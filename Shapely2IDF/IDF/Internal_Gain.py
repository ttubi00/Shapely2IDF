# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 18:00:03 2020

@author: Pink_Blossom
"""

from __future__ import unicode_literals


def __map_internalGain_value(obj, measure_type, my_object, Measure_methods, Props, design_level_method, value):
    """
    Set Value & its type of internal heat gain object (people, lighting, equipment)

    Parameters
    ----------
    obj : str
        IDF object Name (e.g. 'PEOPLE', 'LIGHTS').
    measure_type : str
        internal heat gain type.
    my_object : str
        IDF object (internal heat gain).
    Measure_methods : str
        measurement method.
    Props : str
        Field Name.
    design_level_method : str
        unit of internal heat gain.
    value : float
        value of internal heat gain.

    """

    err_raise = '[__map_internalGain_value] %s in %s object is not invalid. Please check it' %(design_level_method, obj)
    
    try:
        prop_idx = Measure_methods.index(design_level_method)
    except ValueError:    # invalid parameter
        raise Exception(err_raise)
    else: 
        setattr(my_object, measure_type, design_level_method)
        setattr(my_object, Props[prop_idx], value)   


def new_people(idf, use_zonelist = True, n_people_method = 'People/Area', value = 0.2, occ_sche_name = 'Occupancy', 
               act_sche_name = 'Activity', zonelist_name = 'zonelist', default_name = 'people'):
    """
    internal heat gain: people

    Parameters
    ----------
    idf : eppy.modeleditor.IDF
        Eppy's IDF object.
    use_zonelist : bool, optional
        use of ZoneList object (False: use Zone object). The default is True.
    n_people_method : str, optional
        Occupancy counting method. The default is 'People/Area'.
    value : float, optional
        Occupancy value. The default is 0.2.
    occ_sche_name : str, optional
        Occupancy schedule Object Name. The default is 'Occupancy'.
    act_sche_name : str, optional
        Activity schedule Object Name. The default is 'Activity'.
    zonelist_name : str, optional
        ZoneList object Name. The default is 'zonelist'.
    default_name : TYPE, optional
        Object name. The default is 'people'.

    """


    obj = 'people'.upper()

    
    # 측정 방법
    measure_type = 'Number_of_People_Calculation_Method'    

    # 재실자수 단위
    Measure_methods = ['People', 'People/Area', 'Area/Person']

    # IDF field
    Props = ['Number_of_People', 'People_per_Zone_Floor_Area', 'Zone_Floor_Area_per_Person']


    if use_zonelist: # use ZoneList object
        idf.newidfobject(obj) 
        my_object = idf.idfobjects[obj][-1]
        
        # Parameter
        setattr(my_object, 'Name', default_name+'0')
        setattr(my_object, 'Zone_or_ZoneList_Name', zonelist_name)        
        setattr(my_object, 'Number_of_People_Schedule_Name', occ_sche_name)        
        setattr(my_object, 'Activity_Level_Schedule_Name', act_sche_name)                        


        # Matching heat gain value        
        __map_internalGain_value(obj, measure_type, my_object, Measure_methods, Props, n_people_method, value)

                                        
    else: # use zone object
        Zones = idf.idfobjects['zone'.upper()]                
        for idx, zone in enumerate(Zones):
            
            # Add new IDF object
            idf.newidfobject(obj) 
            my_object = idf.idfobjects[obj][-1]
            
            # Parameter
            setattr(my_object, 'Name', default_name+'%d' %(idx))
            setattr(my_object, 'Zone_or_ZoneList_Name', zonelist_name)        
            setattr(my_object, 'Number_of_People_Schedule_Name', occ_sche_name)        
            setattr(my_object, 'Activity_Level_Schedule_Name', act_sche_name)                        

            # Matching heat gain value        
            __map_internalGain_value(obj, measure_type, my_object, Measure_methods, Props, n_people_method, value)



def new_infiltration(idf, sche_name, default_name = 'infiltration', design_level_method = 'AirChanges/Hour', 
                           value = 0.5, use_zonelist = True, zonelist_name = 'zonelist'):
    """
    internal heat gain: infiltration

    Parameters
    ----------
    idf : eppy.modeleditor.IDF
        Eppy's IDF object.
    obj : str
        IDF object Name.
    sche_name : str
        infiltration Schedule Name.
    default_name : str
        Object name. The default is 'infiltration'
    design_level_method : str, optional
        unit of air flow rate. The default is 'AirChanges/Hour'.
    value : float, optional
        infiltration value. The default is 0.5.
    use_zonelist : bool, optional
        use of ZoneList object (False: use Zone object). The default is True.
    zonelist_name : str, optional
        ZoneList object Name. The default is 'zonelist'.

    """


    obj = 'ZoneInfiltration:DesignFlowrate'.upper()


    # 측정 방법
    measure_type = 'Design_Flow_Rate_Calculation_Method'

    # 측정 단위
    Measure_methods = ['Flow/Zone', 'Flow/Area', 'Flow/ExteriorArea', 'Flow/ExteriorWallArea', 'AirChanges/Hour']
    
    # IDF field
    Props = ['Design_Flow_Rate', 'Flow_per_Zone_Floor_Area', 'Flow_per_Exterior_Surface_Area', 'Flow_per_Exterior_Surface_Area', 'Air_Changes_per_Hour']


    if use_zonelist: # use ZoneList object
        idf.newidfobject(obj) 
        my_object = idf.idfobjects[obj][-1]
        
        # Parameter
        setattr(my_object, 'Name', default_name+'0')
        setattr(my_object, 'Zone_or_ZoneList_Name', zonelist_name)        
        setattr(my_object, 'Schedule_Name', sche_name)        


        # Matching heat gain value
        __map_internalGain_value(obj, measure_type, my_object, Measure_methods, Props, design_level_method, value)

    else:  # use zone object
        Zones = idf.idfobjects['zone'.upper()]                
        for idx, zone in enumerate(Zones):
            
            # Add new IDF object
            idf.newidfobject(obj) 
            my_object = idf.idfobjects[obj][-1]
            
            setattr(my_object, 'Name', default_name+'%d' %(idx))
            setattr(my_object, 'Zone_or_ZoneList_Name', getattr(zone, 'Name'))        
            setattr(my_object, 'Schedule_Name', sche_name)          


            # Matching heat gain value        
            __map_internalGain_value(obj, measure_type, my_object, Measure_methods, Props, design_level_method, value)
            


def new_common_iternalGain(idf, obj, sche_name, obj_name, design_level_method = 'Watts/Area', 
                           value = 10, use_zonelist = True, zonelist_name = 'zonelist'):
    """
    internal heat gain: except people & infiltration
    (lights / ElectricEquipment / GasEquipment / SteamEquipment / OtherEquipment)

    Parameters
    ----------
    idf : eppy.modeleditor.IDF
        Eppy's IDF object.
    obj : str
        IDF object Name.
    sche_name : str
        internal heat gain schedule Object Name.
    obj_name : str
        Object name.
    design_level_method : str, optional
        unit of internal heat gain. The default is 'Watts/Area'.        
    value : float, optional
        value of internal heat gain. The default is 10.
    use_zonelist : bool, optional
        use of ZoneList object (False: use Zone object). The default is True.
    zonelist_name : str, optional
        ZoneList object Name. The default is 'zonelist'.

    """
    obj = obj.upper()

    if obj not in ['lights'.upper(), 'ElectricEquipment'.upper(), 'GasEquipment'.upper(), 'SteamEquipment'.upper(), 'OtherEquipment'.upper()]: # warning message & pass (EnergyPlus 9.0기준)
        print('This function not support %s object (Internal Heat Gain). This work will be ignored ' %(obj))

    else:

        # 측정 방법
        measure_type = 'Design_Level_Calculation_Method'

        # 부하 단위 (전기: Watts, 기타: Power)
        dim = 'Watts' if (obj in ['lights'.upper(), 'ElectricEquipment'.upper()]) else 'Power'                        

        # 측정 단위            
        Measure_methods = ['LightingLevel', 'EquipmentLevel', 'Watts/Area', 'Watts/Person']                        

        # IDF field
        Props = ['Lighting_Level', 'Design_Level', '%s_per_Zone_Floor_Area' %(dim), '%s_per_Person' %(dim)]


        #%% Matching internal heat gain information
        if use_zonelist:  # use ZoneList object
        
            # Add new IDF object
            idf.newidfobject(obj) 
            my_object = idf.idfobjects[obj][-1]
        
            # Parameter
            setattr(my_object, 'Name', obj_name+'0')
            setattr(my_object, 'Zone_or_ZoneList_Name', zonelist_name)        
            setattr(my_object, 'Schedule_Name', sche_name)        


            # Matching heat gain value        
            __map_internalGain_value(obj, measure_type, my_object, Measure_methods, Props, design_level_method, value)

        else: # use zone object
            Zones = idf.idfobjects['zone'.upper()]                
            for idx, zone in enumerate(Zones):

                # Add new IDF object
                idf.newidfobject(obj) 
                my_object = idf.idfobjects[obj][-1]
                
                # Parameter
                setattr(my_object, 'Name', obj_name +'%d' %(idx))
                setattr(my_object, 'Zone_or_ZoneList_Name', zonelist_name)        
                setattr(my_object, 'Schedule_Name', sche_name)        

                # Matching heat gain value        
                __map_internalGain_value(obj, measure_type, my_object, Measure_methods, Props, design_level_method, value)
                
                
            