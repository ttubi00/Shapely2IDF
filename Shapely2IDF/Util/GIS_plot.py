# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 21:53:51 2020

@author: Pink_Blossom
"""

from matplotlib import pyplot as plt



def plot_Triangulation(Roof_polygon):
    for sub in Roof_polygon:
        f,a = plt.subplots(1,1, dpi = 500)
        a.plot(sub[:,0], sub[:,1], lw = 5, color = 'k', zorder = 0, label = 'Triangular plane')
        a.plot(sub[[-1,0],0], sub[[-1,0],1], lw = 5, color = 'k', zorder = 0)        
        a.scatter(sub[0,0], sub[0,1], c = 'r', s = 50, edgecolor = 'k', zorder = 1, label = 'Start')
        a.scatter(sub[1,0], sub[1,1], c = 'b', s = 50, edgecolor = 'k', zorder = 1)
        a.scatter(sub[2,0], sub[2,1], c = 'g', s = 50, edgecolor = 'k', zorder = 1, label = 'End')
        a.set_xlabel('X (m)')         
        a.set_ylabel('Y (m)')
        a.legend(loc = 0, fontsize = 'x-small')   
        plt.subplots_adjust(left = 0.2, right = 0.8, top = 0.9, bottom = 0.2, wspace = 0.7, hspace = 0.7)              
        plt.show()