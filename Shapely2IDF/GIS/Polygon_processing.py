# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 16:49:29 2020

@author: Pink_Blossom
"""

import numpy as np
from shapely.ops import triangulate
from shapely.geometry import Point, Polygon


#%%
def np2polygon(XYarray):
    """
     XY array (np.array) -> Shapely Polygon Object

    Parameters
    ----------
    XYarray : np.array [number of vertices, 2]
        xy coordinates.

    Returns
    -------
    polygon : shapely.geometry.polygon.Polygon
        Single Polygon object (w.r.t Shapely).

    """
    polygon = Polygon([tuple(xy) for xy in XYarray])
    return polygon

#%%
def polygon2np(polygon):
    """
    Shapely Polygon Object -> XY array (np.array)
    
    Parameters
    ----------
    polygon : shapely.geometry.polygon.Polygon
        Single Polygon object (w.r.t Shapely).
    xyoffset : np.array
        Offset XY coordinates.        

    Returns
    -------
    XYarray : np.array [number of vertices, 2]
        xy coordinates.

    """
    
    XYarray = np.array(polygon.exterior.xy).T
    XYarray_rev = np.flip(XYarray, axis = 0)
    return XYarray, XYarray_rev


#%% 
def offset_calibration(polygon, xyoffset = np.array([0,0])):
    XY, __ = polygon2np(polygon) - xyoffset
    polygon_offset = np2polygon(XY)
    return polygon_offset
    

#%% 
def point_in_polygon(point, polygon):
    """    
    Determine inside and outside polygons of a point

    Parameters
    ----------
    point : np.array
        XY coordinate (e.g. Centroid of triangular plane).
    polygon : shapely.geometry.polygon.Polygon
        Polygon object (w.r.t Shapely).

    Returns
    -------
    bool
        Whether the XY coordinate is inside or outside the polygon (True: inside, False: outside).

    """
    point_ = Point(point[0], point[1])
    
    return True if polygon.contains(point_) else False


def which_direction(p1, p2, p3):
    """
    Determine Polygon rotation direction (Vector Cross-product, Right hand rule)

    Parameters
    ----------
    p1 : np.array
        1st XY coordinate.
    p2 : np.array
        2nd XY coordinate.
    p3 : np.array
        3rd XY coordinate.

    Returns
    -------
    bool
        True: ClockWise, False: Counter-ClockWise.

    """
    vec1, vec2 = p2-p1, p3-p2 # 좌표 -> 벡터
    vec1 = vec1/np.linalg.norm(vec1) # 벡터 정규화 (크기 n벡터 -> 크기 1 벡터)
    vec2 = vec2/np.linalg.norm(vec2) # 벡터 정규화 (크기 n벡터 -> 크기 1 벡터)

    cross = float(np.cross(vec1, vec2)) # 벡터 외적 (Cross-product)
    return cross < 0 # True: 시계방향, False: 반시계방향



def do_Triangulation(polygon):    
    """    
    Split a single polygon into N triangles (Delaunay triangulation)
    (Single Concave plane -> N convex planes)

    Parameters
    ----------
    polygon : shapely.geometry.polygon.Polygon
        Polygon object (w.r.t Shapely).

    Returns
    -------
    Floor_polygon : List (contents: np.array)
        Triangulated floor XY coordinates.
    Roof_polygon : List (contents: np.array)
        Triangulated roof/ceiling XY coordinates
        (Reverse of the floor polygon).
    """
    
    Triangular_planes = triangulate(polygon) # Polygon의 삼각분할 (들로네 삼각화)

    Floor_polygon, Roof_polygon = [], [] # 삼각분할 된 바닥 및 평면 XY좌표

    #%% 삼각평면 탐색 -> XY좌표 추출
    for idx, tr in enumerate(Triangular_planes):
        sub_polygon, sub_polygon_rev = polygon2np(tr)

        # 중복 좌표 제외
        sub_polygon = sub_polygon[:-1]
        sub_polygon_rev = sub_polygon_rev[:-1]        

        # 삼각평면 중심좌표 
        sub_polygon_centroid = sub_polygon.mean(axis = 0) 

        # 삼각평면 회전방향 수정
        if point_in_polygon(sub_polygon_centroid, polygon) == True: # 삼각평면 중심좌표가 원래 Polygon 내부에 존재
            # sub_polygon_rev = np.flip(sub_polygon, axis = 0) # 회전 방향 반전
            p1, p2, p3 = sub_polygon[0], sub_polygon[1], sub_polygon[2] # 벡터 계산을 위한 3개 좌표 선택 (vec1 = p2-p1, vec2 = p3-p2)
            
            # 삼각평면 좌표의 회전방향 판별 (벡터 외적, Cross product, right hand rule)
            is_Clockwise = which_direction(p1, p2, p3) # 벡터 외적 -> 시계방향 회전 여부 

            # 바닥 & 지붕 -> 삼각평면 추가
            Floor_polygon += [sub_polygon if is_Clockwise == True else sub_polygon_rev]
            Roof_polygon += [sub_polygon_rev if is_Clockwise == True else sub_polygon]

    return Floor_polygon, Roof_polygon  

