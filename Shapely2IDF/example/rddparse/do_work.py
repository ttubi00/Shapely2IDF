# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 02:47:26 2020

@author: Pink_Blossom
"""

from Shapely2IDF.Util.ExternalData_ import rdd_parse, rdd2Json


rddfname = 'toy.rdd'
outputs = rdd_parse(rddfname)

json_fname = 'my.json'
my_dict = rdd2Json(outputs, json_fname)