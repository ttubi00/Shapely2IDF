# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 17:38:53 2020

@author: Pink_Blossom
"""

import numpy as np



def calc_wall_shift(wall_area, wall_height, wwr):
    """
    Wall dimension information & Window-wall ratio -> Exterior wall-window gap
    (Given {Wall area, Wall height, Window-wall ratio} -> Quadratic equation -> XY coordinate shifting depth)
    
    -------WALL----------
    - d               d -
    -d*****************d-      
    - * Win_area =    * -
    - * wall_area*wwr * -
    - *               * -    
    -d*****************d-
    - d               d -      
    ---------------------
    
    Parameters
    ----------
    wall_area : float
        Wall area (m2).
    wall_height : float
        Wall height (= zone height, m).
    wwr : float
        Window-wall ratio  (0~1).

    Returns
    -------
    d_: float
        depth from wall-edge to window-edge (m).

    """

    width = wall_area / wall_height # 외벽 너비
    p = [4, -(2*width + 2*wall_height), (1-wwr)*wall_area] # p[0]*D^2 + p[1]*D + p[-1] = 0
    D = np.roots(p) # real solution & dummy solution (np.roots: Polynomial equation solver)
   
    d_ = float(D[np.where((width - 2*D) > 0)]) # real solution (shifting 시켰을 때, 잔여 너비의 +값 여부)
    
    return d_


def hr_2digit(hr):
    """
    [W.R.T. Schedule:compact], Hour (integer) -> Str ('01', '02',..'24')

    Parameters
    ----------
    hr : float or int
        Hour.

    Returns
    -------
    str_hr : str
        Hour converted to Str.

    """
    str_hr = str(int(hr)) if hr > 10 else '0' + str(int(hr))
    return str_hr



def CMH2CMS(cms):
    """
    Cubic Meter per Hour -> Cubic Meter per Second (volume conversion)

    Parameters
    ----------
    cmh : float
        air flow rate per area (m3/m2s).

    Returns
    -------
    float
        air flow rate per area (m3/m2h).

    """
    return cms/3600    






