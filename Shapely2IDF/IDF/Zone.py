# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 17:45:38 2020

@author: Pink_Blossom
"""


def new_zone(idf, zname, zheight = 3.5):
    """
    Generate a new zone (Eppy's IDF object')

    Parameters
    ----------
    idf : eppy.modeleditor.IDF
        Eppy's IDF object.
    zname : int
        zone index (1st floor: 0, 2nd floor: 1,...).

    """

    #%% Add new IDF object
    obj = 'zone'.upper()

    idf.newidfobject(obj)
    my_object = idf.idfobjects[obj][-1]
    
    #%% Zone origion (XY = [0,0], Z = zheight * (zname-1))
    Zorigin = zheight * zname 
    
    #%% Zone parameter
    setattr(my_object, 'Name', str(zname))    
    setattr(my_object, 'Z_Origin', str(Zorigin))
    



def gen_zonelist(idf, default_value = 'zonelist', Zidx = []):
    """
    Generate IDF ZoneList Object (To make the integrated zone management easier, {Internal heat gains})
    if no user-define zone list, then all zones will be integrated

    Parameters
    ----------
    idfobj : eppy.bunch_subclass.EpBunch
        Eppy's schedule compact object.
    default_value : TYPE, optional
        Object Name. The default is 'zonelist'.
    Zidx : List, optional
        User-define Zone Object index. The default is [].
    """


    #%% Zone 존재여부 확인 -> 존이 존재하지 않는다면 -> warning message & pass
    err_raise = '[gen_zonelist] No zone exists. Please construct zones before.'

    zones = idf.idfobjects['zone'.upper()]
    n_zone = len(zones)

    if n_zone == 0:  # empty zones
        raise Exception(err_raise)

    else:          
        #%% Add new IDF object
        obj = 'zonelist'.upper()
        idf.newidfobject(obj) 
        my_object = idf.idfobjects[obj][-1]    

        setattr(my_object, 'Name', default_value)

        #%% Matching zones to Zone list

        if len(Zidx) == 0: # all zones integration (i.e. 모든 존 통합)        
            [setattr(my_object, 'Zone_%d_Name' %(idx+1), getattr(zone, 'Name')) for idx, zone in enumerate(zones)]  

        else: # apply user-define zones
            [setattr(my_object, 'Zone_%d_Name' %(idx+1), getattr(zones[zidx], 'Name')) for idx, zidx in enumerate(Zidx)]    
    


