# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 00:03:42 2020

@author: Pink_Blossom
"""

def set_Site_location(idf, name, lat, lon, tzone, elev):
    """
    Set Site:location IDF object

    Parameters
    ----------
    idf : eppy.modeleditor.IDF
        Eppy's IDF object.
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
    obj = 'Site:location'.upper()
    idfobj = idf.idfobjects[obj][0]

    setattr(idfobj, 'Name', name)
    setattr(idfobj, 'Latitude', lat)
    setattr(idfobj, 'Longitude', lon)
    setattr(idfobj, 'Time_Zone', tzone)    
    setattr(idfobj, 'Elevation', elev)        
    