# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 20:01:04 2020

@author: Pink_Blossom
"""

#%%
# Compatibility between python2 and python3 (Print command)
from __future__ import print_function

# Import method from Shapely2IDF module
from Shapely2IDF.GIS.Polygon_processing import polygon2np, do_Triangulation, offset_calibration

from Shapely2IDF.Material.Default_IDF import get_minimalIDF

from Shapely2IDF.IDF.LoadIDF import gen_idf
from Shapely2IDF.IDF.Geometry import build_mass, build_shadingObj
from Shapely2IDF.IDF.Zone import gen_zonelist
from Shapely2IDF.IDF.Schedule import build_schedule_compact_dict
from Shapely2IDF.IDF.Internal_Gain import new_people, new_common_iternalGain, new_infiltration
from Shapely2IDF.IDF.HVAC import HVAC_IdealLoadsAirSystem, HVAC_Thermostat, set_Sim_control
from Shapely2IDF.IDF.Site import set_Site_location
from Shapely2IDF.IDF.Material import insulation_thickness
from Shapely2IDF.IDF.Fenestration import SimpleGlazing_all, SimpleGlazing_each
from Shapely2IDF.IDF.Output import set_Output_Variable

from Shapely2IDF.Util.ExternalData_ import MakeDict_schedule_compact_From_ExternalForm, Dict_schedule_compact2JSON, get_location_epw
from Shapely2IDF.Util.GIS_plot import plot_Triangulation
from Shapely2IDF.Util.Value import CMH2CMS # m3/m2h -> m3/m2s
from Shapely2IDF.Util.Uvalue import WallUvalue_material, FloorUvalue_material, RoofUvalue_material

# Import auxiliary modules
import pickle
import os
import numpy as np
import time


#%% tic toc
tic = time.time()

#%% GIS데이터 로드 (Shapely.Polygon) -> 본 예제에서는 사전에 Pickle 파일로 직렬화

# 대상건물 (Shapely.Polygon -> GIS)
my_building = pickle.load(open('my_building.dat', 'rb')) 

# 인접건물들 (2개 건물, List of Shapely.Polygon)
shading_objs = pickle.load(open('shading_obj.dat', 'rb')) 


#%% offset 수정

# XY좌표 오프셋 (기상대 위치에 대응)
xyoffset = np.array([199971.0114, 452219.862 ]) 

# polygon 재설정 (오프셋 보정, shapely.Polygon or [shapely.Polygon])
my_building = offset_calibration(my_building, xyoffset) # 대상건물
shading_objs = [offset_calibration(shd_obj, xyoffset) for shd_obj in shading_objs] # 인접건물들



#%% GIS -> np.array (인접건물들: List of np.arrays (복수 건물이므로))
XY, XY_rev = polygon2np(my_building) # 대상건물 외벽 구성에 활용

shading_footprints = [ polygon2np(shd_obj)[1] for shd_obj in shading_objs  ] # 인접건물 외벽 구성에 활용


#%% Polygon -> 삼각분할 (볼록 평면화) -> 지붕/바닥 구성에 활용
Floor_subs, Roof_subs = do_Triangulation(my_building) # 분할 삼각평면 (np.array)
print('The polygon was divided into %d triangular planes.\n' %(len(Floor_subs)))

plot_Triangulation(Roof_subs) # 삼각분할 결과 가시화

#%% 소스파일로부터 IDF (minimal.idf) 및 IDD파일 로드 (v9.0) 

savepath = os.getcwd() # 현재 폴더
idfname, iddname = get_minimalIDF(savepath) # 소스파일로부터 IDF & IDD파일 복사


#%% Eppy -> IDF object 생성
# 사용자 IDF 및 IDD파일 직접 적용 가능 
idf, IDF_ = gen_idf(idfname, iddname)


#%% Step 1. Geometry modeling (Zone & Surfaces)
# 사용자 입력
n_floor = 3 # 대상건물 층수 (w.r.t 건축물 대장정보)
wwr = 0.5 # 창면적비 (0~1)
zheight = 3.5 # 존 층고 (3.5m)

const_wall = 'exwall' # 외벽 construction name (default: in minimal.idf)
const_window = 'exwin' # 창호 construction name (default: in minimal.idf)


# 모델링
build_mass(idf, n_floor, Floor_subs, Roof_subs, XY_rev, wwr, zheight, const_wall, const_window)


# Zonelist 생성 (IF n_floor==3, THEN zone name = [0, 1, 2])
zonelist = 'zonelist'
gen_zonelist(idf, zonelist)


#%% Step 2. Shading object modeling
# 사용자 입력
n_floors = [3, 4] # 인접 건물들의 층수 (건축물 대장 정보)
zheight_shading = 3.5 # 인접 건물 존 층고 (default = 3.5m)
objname_prefix = 'Shading' # Shading object name 접두사
Transmittance_ScheName = None # 인접건물 일사투과 스케쥴 이름


# 모델링
build_shadingObj(idf, shading_footprints, n_floors, zheight_shading, objname_prefix, Transmittance_ScheName = None)


#%% Step 3. Schedule compact 모델링 (use external data)

# Schedule comapact 데이터 로드 (Excel form -> dictionaries)
fname2 = 'test.xlsx' # User-input schedule compact information
Sche_Dicts, Sche_names, TypeLimits = MakeDict_schedule_compact_From_ExternalForm(fname2) 

print('Schedule compact: object names')
print(Sche_names)
print('')

# (Optional) Schedule compact 데이터 -> JSON 파일로 출력
Dict_schedule_compact2JSON(Sche_Dicts)

# Build schedule compact objects
for Sche_Dict, TypeLimit in zip(Sche_Dicts, TypeLimits):
    build_schedule_compact_dict(idf, Sche_Dict, TypeLimit)


# Schedule compact name
occ_sc = Sche_names[0] # People (occpancy)
act_sc = Sche_names[1] # People (activity)
light_sc = Sche_names[2] # (Interior) Lighting
equip_sc = Sche_names[3] # Electric equipment
infil_sc = Sche_names[4] # Infiltration
hvac_sc = Sche_names[5] # HVAC operation
cool_sc = Sche_names[6] # Cooling system operation
heat_sc = Sche_names[7] # Heating system operation
coolSP_sc = Sche_names[8] # Cooling setpoint
heatSP_sc = Sche_names[-1] # Heating setpoint


#%% Step 4. Internal heat gain 모델링 (인체, 조명, 기기, 침기) 

# Heat gain value
occ_val = 0.2 # 0.2 people/m2
light_val = 10 # 10W/m2
equip_val = 10 # 10W/m2
infil_val = 0.5 # 0.5 ACH


# Heat gain unit
occ_unit = 'People/Area'
light_unit = 'Watts/Area'
equip_unit = 'Watts/Area'
infil_unit = 'AirChanges/Hour'


# Heat gain IDF object name (접두사, 예: 'people' -> 1층: 'people0', 2층: 'people1',...) 
occ_prefix = 'people'
light_prefix = 'light'
equip_prefix = 'equip'
infil_prefix = 'infiltration'


# Internal heat gain IDF object 생성 (Tutorial 목적으로, 함수 별 모든 parameter 정의)
new_people(idf, use_zonelist = True, n_people_method = occ_unit, value = occ_val, 
           occ_sche_name = occ_sc, act_sche_name = act_sc, zonelist_name = zonelist, 
           default_name = occ_prefix)


new_common_iternalGain(idf, obj = 'lIghTS', sche_name = light_sc, obj_name = light_prefix, 
                       design_level_method = light_unit, value = light_val, use_zonelist = True, zonelist_name = zonelist)
    

new_common_iternalGain(idf, obj = 'electricequipment', sche_name = equip_sc, obj_name = equip_prefix, 
                       design_level_method = equip_unit, value = equip_val, use_zonelist = True, zonelist_name = zonelist)


new_infiltration(idf, sche_name = infil_sc, default_name = infil_prefix, 
                 design_level_method = infil_unit, value = infil_val, use_zonelist = True, zonelist_name = zonelist)



#%% Step 5. HVAC 모델링 (Simulation control & Thermostat & IdealloadsAirsystem)
# Simulation control
set_Sim_control(idf) # default: Setting for running IdealLoadsAirsystem simulation)

# Thermostat
thermo_name = 'thermo' # IDF object name
HVAC_Thermostat(idf, default_name = thermo_name, Heat_setpoint_sche = heatSP_sc, Cool_setpoint_sche = coolSP_sc)


# IdealloadsAirsystem
prefix_idealloads = 'IdealLoadsAirSystem' # IDF object name (접두사)
is_OA_use = True # 외기도입 여부 (HVAC)
OA_volume = 6 # 1인당 m3/m2h (외기도입량)
OA_volume = CMH2CMS(OA_volume) # 외기도입량 m3/m2s로 단위 환산 (EnergyPlus OA object 참조)

HVAC_IdealLoadsAirSystem(idf, default_name = prefix_idealloads, thermostat_Name = thermo_name, HVACSche = hvac_sc, 
                             HeatSche = hvac_sc, CoolSche = cool_sc, is_OA_use = is_OA_use, OA_measure = 'Flow/Person', OA_method = 'Outdoor_Air_Flow_Rate_per_Person', OA_value = OA_volume)



#%% Step 6. Site:location 모델링 (from epw file)
epwname = 'USA_CO_Denver-Stapleton.724690_TMY.epw'
name, lat, lon, tzone, elev = get_location_epw(epwname) # 지역이름, 위도, 경도, 시간대(time zone), 고도

set_Site_location(idf, name, lat, lon, tzone, elev)


#%% Step 7. 외피 단열 (창호: U-value수정, 기타: 단열재 두께 수정)
# 외벽/지붕/바닥 Target U-value (W/m2K) 
Wall_U = 0.1
Roof_U = 0.2
Floor_U = 0.3

#%% Step 7.1 외벽/지붕/바닥 단열 속성

# 외벽/지붕/바닥 단열재 object name
Wall_insName = 'I02 50mm insulation board' # conductivity: 0.03W/mK
Roof_insName = 'I02 50mm insulation board_roof' # conductivity: 0.03W/mK
Floor_insName = 'I02 50mm insulation board_floor' # conductivity: 0.03W/mK


# 외벽/지붕/바닥 단열재 요구 두께 계산 (m, ASHRAE HOF 2005 Medium type 가정. 단, 지붕/바닥 단열재 종류는 외벽과 동일하다고 가정)
Wall_d = WallUvalue_material(Wall_U)
Roof_d = RoofUvalue_material(Roof_U)
Floor_d = FloorUvalue_material(Floor_U) 


# 외벽/지붕/바닥 단열재 두께 업데이트
insulation_thickness(idf, Wall_d, ins_name = Wall_insName)
insulation_thickness(idf, Roof_d, ins_name = Roof_insName)
insulation_thickness(idf, Floor_d, ins_name = Floor_insName)


#%% Step 7.2 창호 단열 속성

# 창호 Target U-value (W/m2K) & SHGC 
Win_U, Win_SHGC = 1.2, 0.4

# 창호 단열 속성 업데이트 (모든 창호 일괄 업데이트)
SimpleGlazing_all(idf, Uvalue = Win_U, SHGC = Win_SHGC)

## 창호 단열 속성 업데이트 (창호 개별 업데이트)
# Win_name = 'fenestration'
# SimpleGlazing_each(idf, objname = Win_name, Uvalue = Win_U, SHGC = Win_SHGC)


#%% Step 8 모델 출력 설정 (Output: Variable)
My_outputs = ['Zone Ideal Loads Zone Total Heating Energy ', 'Zone Ideal Loads Zone Total Cooling Energy' ]
[set_Output_Variable(idf, output) for output in My_outputs]


#%% Step 9. IDF save
newIDFname = 'toy.idf'
idf.saveas(newIDFname)

#%% toc
toc = time.time()
print('Running time: %.3fSec' %(toc-tic))


