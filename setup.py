# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 03:29:30 2020

@author: Pink_Blossom
"""

from distutils.core import setup

files = ['Material/*', 'example/*', 'example/rddparse/*']


setup(
    name                = 'Shapely2IDF',
    version             = '0.11',
    description         = 'IDF generator based on Shapely Polygon (EnergyPlus)',
    author              = 'Pink_Blossom',
    author_email        = 'donghyuk.yi3014@snu.ac.kr',
    install_requires    =  ['shapely == 1.7.0', 'numpy == 1.18.5', 'pandas == 1.0.5', 'eppy == 0.5.52', 'pip==9.0.3', 'matplotlib==3.2.2'],
    packages=[
        'Shapely2IDF',
        'Shapely2IDF.example',
        'Shapely2IDF.GIS',
        'Shapely2IDF.IDF',
        'Shapely2IDF.Material',
        'Shapely2IDF.test',
        'Shapely2IDF.Util',
    ],
    package_data = {'Shapely2IDF' : files},
    keywords            = ['Shapely2IDF', 'EnergyPlus', 'GIS', 'shapely'],
    python_requires     = '>=3',
    include_package_data= True,
    zip_safe            = False,
    classifiers         = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',        
    ],
)