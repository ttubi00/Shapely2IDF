# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 22:14:10 2020

@author: Pink_Blossom
"""

from .Zone import new_zone
import numpy as np
from ..Util.Value import calc_wall_shift




def gen_vertex(surface_obj, vertex_idx, xyz, value):
    """
    Set XYZ vertex to specific IDF surface object 
    (buildingsurface:detailed, fenestration:detailed)

    Parameters
    ----------
    surface_obj : eppy.bunch_subclass.EpBunch'
        Eppy's idfobjects (surface).
    vertex_idx : int
        vertex sequence.
    xyz : str
        vertex type ('x', 'y', 'z').
    value : float
        vertex value.
    """
    
    field = 'Vertex_%d_%scoordinate' %(vertex_idx, xyz.upper())
    setattr(surface_obj, field, value)




def build_mass(idf, n_floor, Floor_subs, Roof_subs, XY_rev, wwr = 0.5, zheight = 3.5, const_wall = 'exwall', const_window = 'exwin'):

    # number of plane vertices
    n_p = XY_rev.shape[0] 


    # Creating zones and skins for each floor
    for zname in range(n_floor):

        #%% Create new zone for each floor
        new_zone(idf, zname)        

        # Setting Surface adjacent condition (floor, roof, ceiling)
        if zname == 0: # Ground floor
            const_floor, const_roof = 'exfloor', 'ceiling'
            surtype_floor, surtype_roof = 'Floor', 'Ceiling'    
            bndcond_floor, bndcond_roof = 'Ground', 'Surface'
        elif (zname > 0) & (zname < n_floor-1): # Mid floor
            const_floor, const_roof = 'intfloor', 'ceiling'
            surtype_floor, surtype_roof = 'Floor', 'Ceiling'    
            bndcond_floor, bndcond_roof = 'Surface', 'Surface'    
        else: # Top floor
            const_floor, const_roof = 'intfloor', 'exroof'
            surtype_floor, surtype_roof = 'Floor', 'Roof'    
            bndcond_floor, bndcond_roof = 'Surface', 'Outdoors'                
            
        
        #%% Build Horigonzal surfaces (floor, roof, ceiling)
        for idx, (Floor_sub, Roof_sub) in enumerate(zip(Floor_subs, Roof_subs)):
            n_vertices = Floor_sub.shape[0]
            new_horizontal_surface(idf, zname, idx, Floor_sub, zheight, constname = const_floor, n_vertices = n_vertices, 
                                   surtype = surtype_floor, bndcond = bndcond_floor)
            new_horizontal_surface(idf, zname, idx, Roof_sub, zheight, constname = const_roof, n_vertices = n_vertices, 
                                   surtype = surtype_roof, bndcond = bndcond_roof)

        #%% Build Vertical surfaces (wall & window)
        for idx in range(n_p-1):
            p1, p2 = XY_rev[idx], XY_rev[idx+1]

            new_vertical_surface(idf, zname, idx, p1, p2, zheight, wwr, const_wall, const_window, n_vertices = 4, surtype1 = 'Wall', surtype2 = 'Window', bndcond = 'Outdoors')
            

            
def new_horizontal_surface(idf, zname, idx, XY, zheight = 3.5, constname = 'exfloor', n_vertices = 3, surtype = 'Floor', bndcond = 'Ground'):
    """
    New horizontal surfaces (Roof, Floor, Ceiling)

    Parameters
    ----------
    idf : eppy.modeleditor.IDF
        Eppy's IDF object.
    zname : int
        Zone index (e.g. floor 1: 0, floor 2: 1).
    idx : int
        Surface index.
    XY : np.array
        XY verteces [number of vertices, 2].
    zheight : float, optional
        Zone heights. The default is 3.5m.
    constname : str, optional
        IDF Construction name. The default is 'exfloor'.
    n_vertices : int, optional
        Number of XY verteces (Triangular: 3). The default is 3.
    surtype : str, optional
        Surface type ('Floor'; 'Ceiling'; 'Roof') . The default is 'Floor'.
    bndcond : str, optional
        outside condition (Ground; Outdoors; Surface) . The default is 'Ground'.
    """

    #%% IDF objects 생성
    obj = 'buildingsurface:detailed'.upper()
    idf.newidfobject(obj)
    my_object = idf.idfobjects[obj][-1]

    #%% 객체 이름 
    surname = '%s_%s%d' %(zname, surtype, idx)


    #%% 인접 외피 & 외부 기후정보 매칭   

    outside_bndcond = '' # default: 인접 외피 없음 (Ground or Outdoor)

    if bndcond == 'Surface':
        sun_exposure, wind_exposure = 'NoSun', 'NoWind'
        
        adj_surface = 'Floor' if surtype =='Ceiling' else 'Ceiling'
        outside_bndcond = '%d_%s%d' %(zname+1, adj_surface, idx) if surtype =='Ceiling' else '%d_%s%d' %(zname-1, adj_surface, idx)

    else: # Ground or Outdoors
        sun_exposure, wind_exposure = ('NoSun', 'WindExposed') if bndcond == 'Ground' else ('SunExposed', 'WindExposed')
    

    

    #%% 지붕/바닥/천장 파라미터    
    setattr(my_object, 'Name', surname)    
    setattr(my_object, 'Surface_Type', surtype)            
    setattr(my_object, 'Construction_Name', constname)                
    setattr(my_object, 'Zone_Name', zname)        
    setattr(my_object, 'Outside_Boundary_Condition', bndcond)            
    setattr(my_object, 'Outside_Boundary_Condition_Object', outside_bndcond)                
    setattr(my_object, 'Sun_Exposure', sun_exposure)                
    setattr(my_object, 'Wind_Exposure', wind_exposure)                    
    setattr(my_object, 'Number_of_Vertices', n_vertices)  

    #%% 지붕/바닥/천장 z좌표
    z = zheight if (surtype == 'Ceiling') | (surtype == 'Roof') else 0


    #%% 지붕/바닥/천장 평면좌표 매칭
    Xs, Ys = XY[:,0], XY[:,1] # X & Y 좌표들

    for vertex_idx, (x, y) in enumerate( zip(Xs, Ys) ):
        gen_vertex(my_object, vertex_idx+1, 'x', x)                       
        gen_vertex(my_object, vertex_idx+1, 'y', y)                               
        gen_vertex(my_object, vertex_idx+1, 'z', z)                                       


#%%
def new_vertical_surface(idf, zname, idx, p1, p2, zheight = 3.5, wwr = 0, constname1 = 'exwall', constname2 = 'exwin', n_vertices = 4, surtype1 = 'Wall', surtype2 = 'Window', bndcond = 'Outdoors'):
    """
    New vertical surfaces (Exterior wall, Fenestration)

    Parameters
    ----------
    idf : eppy.modeleditor.IDF
        Eppy's IDF object.
    zname : int
        Zone index (floor 1: 0, floor 2: 1).
    idx : int
        surface index (Wall, Fenestration).
    p1, p2 : np.array
        1st & 2nd XY verteces (w.r.t Polygon).
    zheight : float, optional
        Zone heights. The default is 3.5m.
    wwr : float, optional
        Window-wall ratio. The default is 0 (no windows).
    constname1 : str, optional
        IDF Construction name (Wall). The default is 'exwall'.
    constname2 : str, optional
        IDF Construction name (Fenestration). The default is 'exwin'.
    n_vertices : int, optional
        Number of XY verteces (Rectangular: 4). The default is 4.
    surtype1 : str, optional
        Surface type ('Wall'). The default is 'Wall'.
    surtype2 : str, optional
        SubSurface type ('Window', Door, GlassDoor, TubularDaylightDome, TubularDaylightDiffuser). 
                        The default is 'Window'.
    bndcond : str, optional
        Outside condition. The default is 'Outdoors'.
    """


    #%% IDF objects label
    obj1 = 'buildingsurface:detailed'.upper()
    obj2 = 'fenestrationsurface:detailed'.upper()

    #%% 객체 이름
    surname1 = '%d_%s%d' %(zname, surtype1, idx) # 외벽
    surname2 = '%d_%s%d' %(zname, surtype2, idx) # 창
    

    #%% 외벽 표면 조건 설정   
    outside_bndcond = '' # default: 인접 외피 없음 (Outdoor)

    sun_exposure, wind_exposure = ('NoSun', 'NoWind') if bndcond == 'Surface' else ('SunExposed', 'WindExposed')

    
    #%% 신규 외벽 객체 생성
    idf.newidfobject(obj1) # 외벽

    
    #%% 신규 외벽 객체 선택
    my_object1 = idf.idfobjects[obj1][-1]


    #%% Z 좌표 (low & high)
    z1, z2 = 0, zheight


    #%% 외벽 파라미터   
    setattr(my_object1, 'Name', surname1)    
    setattr(my_object1, 'Surface_Type', surtype1)            
    setattr(my_object1, 'Construction_Name', constname1)                
    setattr(my_object1, 'Zone_Name', zname)        
    setattr(my_object1, 'Outside_Boundary_Condition', bndcond)            
    setattr(my_object1, 'Outside_Boundary_Condition_Object', outside_bndcond)                
    setattr(my_object1, 'Sun_Exposure', sun_exposure)                
    setattr(my_object1, 'Wind_Exposure', wind_exposure)                    
    setattr(my_object1, 'Number_of_Vertices', n_vertices)  
    
    

    #%% 외벽 좌표 배치 (Start: UpperLeftCorner, Rotation: CounterClockWise)
    gen_vertex(my_object1, 1, 'x', p2[0])     
    gen_vertex(my_object1, 1, 'y', p2[1])                               
    gen_vertex(my_object1, 1, 'z', z2)            

    gen_vertex(my_object1, 2, 'x', p1[0])     # Upper left (from Outdoor to Zone view)                
    gen_vertex(my_object1, 2, 'y', p1[1])                               
    gen_vertex(my_object1, 2, 'z', z2)                    

    gen_vertex(my_object1, 3, 'x', p1[0])                       
    gen_vertex(my_object1, 3, 'y', p1[1])                               
    gen_vertex(my_object1, 3, 'z', z1)        

    gen_vertex(my_object1, 4, 'x', p2[0])     
    gen_vertex(my_object1, 4, 'y', p2[1])                               
    gen_vertex(my_object1, 4, 'z', z1)      
    

    #%% 창호 생성 여부
    if (wwr != 0) & (wwr > 0) & (wwr < 1): # 창면적비 입력 & 입력 창면적비 유
    
        #%% 신규 창호 객체 생성
        idf.newidfobject(obj2) # 창호   
        my_object2 = idf.idfobjects[obj2][-1]
    

        #%% 외벽좌표 -> 창호 좌표 shifting 길이 계산 (외벽 좌표 -> 상하좌우 균등 이동 -> 창호 좌표)
        wall_height = z2-z1
        wall_area = np.linalg.norm(p2-p1) * wall_height # 너비: 벡터 크기 (norm), 면적 = 너비*높이
    
        d = calc_wall_shift(wall_area, wall_height, wwr) # 외벽 좌표 shifting 길이 (m)

        C = np.linalg.norm(p2-p1)

        #%% XY좌표 Shifing (삼각함수 활용)
    
        '''
        
        ^  -
        -  -        *
        Y  B   C *
        -  - *
        -  *----A-----
        --------------------X--->

        Vector C = p2-p1        
        Cosine   = C/A
        Sine     = C/B 
        shift_x  = d*Cosine
        shift_y  = d*Sine        
        shift_z  = d
                
        '''
    
    
        # 원점이동 & XY벡터 삼각함수 계산
        A = (p2-p1)[0]
        B = (p2-p1)[1]
        cos, sin = A/C, B/C

        # 평면좌표 Shifting
        XYshift = np.array([d*cos, d*sin])
        p1_, p2_ = p1+XYshift, p2-XYshift # 창호 XY 좌표 (shifting 결과)
        
        # Z좌표 Shifting
        z1_, z2_ = z1+d, z2-d


        # 창호 파라미터   
        setattr(my_object2, 'Name', surname2)    
        setattr(my_object2, 'Surface_Type', surtype2)            
        setattr(my_object2, 'Construction_Name', constname2)                
        setattr(my_object2, 'Building_Surface_Name', surname1) # 외벽객체 이름                
        setattr(my_object2, 'Number_of_Vertices', n_vertices)      

        # 창호 좌표 배치 (Start: UpperLeftCorner, Rotation: CounterClockWise)
        gen_vertex(my_object2, 1, 'x', p2_[0])     
        gen_vertex(my_object2, 1, 'y', p2_[1])                               
        gen_vertex(my_object2, 1, 'z', z2_)            

        gen_vertex(my_object2, 2, 'x', p1_[0])     # Upper left (from Outdoor to Zone view)                
        gen_vertex(my_object2, 2, 'y', p1_[1])                               
        gen_vertex(my_object2, 2, 'z', z2_)                    

        gen_vertex(my_object2, 3, 'x', p1_[0])                       
        gen_vertex(my_object2, 3, 'y', p1_[1])                               
        gen_vertex(my_object2, 3, 'z', z1_)        

        gen_vertex(my_object2, 4, 'x', p2_[0])     
        gen_vertex(my_object2, 4, 'y', p2_[1])                               
        gen_vertex(my_object2, 4, 'z', z1_)     

    elif (wwr < 0) | (wwr > 1): # 입력된 창면적비가 유효하지 않음 -> warning message & pass
        print('input Window-Wall ratio is not invalid')      
    else: # 창면적비 미입력 -> warning message & pass
        print('input Window-Wall ratio is empty. Walls will be generated only')      
        

#%%
def new_shading_object(idf, idx, subidx, p1, p2, n_floor, default_name = 'Shading', zheight = 3.5, Transmittance_ScheName = None, n_vertices = 4):  
    """
    New shading object (adjacent buildings)

    Parameters
    ----------
    idf : eppy.modeleditor.IDF
        Eppy's IDF object.
    idx : int
        Shading object index.
    subidx : int
        Shading objects' surface indices.
    p1 : np.array
        1st XY vertex of object's footprint.
    p2 : np.array
        2nd XY vertex of object's footprint.
    n_floor : int
        Number of floors.
    default_name : str, optional
        Shading object's name (prefix). The default is 'Shading'.
    zheight : float, optional
        Zone heights. The default is 3.5.
    Transmittance_ScheName : str, optional
        Transmittance schedule object. The default is None (i.e. AllWays opaque).
    n_vertices : int, optional
        Number of verteces w.r.t. (vertical) each surface (Retanguar: 4). The default is 4.

    """


    #%% IDF objects 생성
    obj = 'Shading:Building:Detailed'.upper()


    #%% 신규 인접건물 객체 생성 (Shading object)
    idf.newidfobject(obj)

    
    #%% 신규 외벽 객체 선택
    my_object1 = idf.idfobjects[obj][-1]


    #%% Z 좌표 (low & high)
    z1, z2 = 0, zheight*n_floor


    # 인접건물 파라미터 (Shading object)
    setattr(my_object1, 'Name', '%s%d_%d' %(default_name, idx, subidx) )    
    setattr(my_object1, 'Transmittance_Schedule_Name', Transmittance_ScheName) if Transmittance_ScheName != None else 1+1            
    setattr(my_object1, 'Number_of_Vertices', n_vertices)  
    
    

    #%% 외벽 좌표 배치 (Start: UpperLeftCorner, Rotation: CounterClockWise)
    gen_vertex(my_object1, 1, 'x', p2[0])     
    gen_vertex(my_object1, 1, 'y', p2[1])                               
    gen_vertex(my_object1, 1, 'z', z2)            

    gen_vertex(my_object1, 2, 'x', p1[0])     # Upper left (from Outdoor to Zone view)                
    gen_vertex(my_object1, 2, 'y', p1[1])                               
    gen_vertex(my_object1, 2, 'z', z2)                    

    gen_vertex(my_object1, 3, 'x', p1[0])                       
    gen_vertex(my_object1, 3, 'y', p1[1])                               
    gen_vertex(my_object1, 3, 'z', z1)        

    gen_vertex(my_object1, 4, 'x', p2[0])     
    gen_vertex(my_object1, 4, 'y', p2[1])                               
    gen_vertex(my_object1, 4, 'z', z1)    




def build_shadingObj(idf, Footprints, n_floors, zheight = 3.5, default_name = 'Shading', Transmittance_ScheName = None):
    """
    Build shading object using Foorprint data (conversioned from Polygon)
    -> In mass modeling, "new_shading_object" will be used

    Parameters
    ----------
    idf : eppy.modeleditor.IDF
        Eppy's IDF object.
    Footprints : list[np.array]
        Shading objects' XY verteces.
    n_floors : list[int]
        Number of floors for each shading object.
    zheight : float, optional
        Zone height. The default is 3.5m.
    default_name : str, optional
        Shading object's name (prefix). The default is 'Shading'.
    Transmittance_ScheName : str, optional
        Transmittance schedule object. The default is None (i.e. AllWays opaque).

    Raises
    ------
    Exception
        input dimension Inequality.
    """

    err_raise = '[build_shadingObj] lengths of (Shd_objs & n_floors) are not equal'    

    # 인접건물 객체와 층수 정보 일치여부 검사 (check List lengths equality)
    if len(Footprints) != len(n_floors):
        raise Exception(err_raise) # error raise

    # 인접건물 탐색 -> 외벽 생성 (차폐물)

    for shd_idx, (Footprint, n_floor) in enumerate(zip(Footprints, n_floors)): # len(Shd_objs) == len(n_floors)

        # Polygon 좌표 수 (외벽 생성 목적)
        n_p = Footprint.shape[0] 

        # 좌표 탐색
        for sur_idx in range(n_p-1):
            p1, p2 = Footprint[sur_idx], Footprint[sur_idx+1] # 전/후 좌표 (외벽 가로방향 좌표)
            new_shading_object(idf, shd_idx, sur_idx, p1, p2, n_floor, default_name, zheight, Transmittance_ScheName, n_vertices = 4)    
