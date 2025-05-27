# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 08:45:52 2024

@author: elisa.borlat
"""


from lib.data_manager import DataManager
import lib.compute_normal_height as height

#### Load data from Excel file
data_manager = DataManager()
data_manager.load_data('EVRF2019_Summary_Schweiz.xlsx')

#--------------
# Sheet LHN95-DEF
#-------------- 

#### Compare Hnorm from sheet and Hnorm compute from Pot
df_pot = data_manager.data.get('LHN95_Pot')
df_lat = data_manager.data.get('EVRF_trans_lat')
df_filtered = data_manager.data[(df_pot.notna()) & (df_lat.notna())].copy()
h_compute = []
for index, row in df_filtered.iterrows():
    h = height.compute_normal_height_from_pot(row['LHN95_Pot']*10.0, row['EVRF_trans_lat'],log=False)
    h_compute.append(h)
df_filtered.loc[:, 'Computed_Height'] = h_compute
df_normal = data_manager.data.get('LHN95_Hnorm').notna()

# Vérification
print(df_filtered[['LHN95_Pot', 'EVRF_trans_lat', 'Computed_Height', 'LHN95_Hnorm']])  # not equal

'''
La différence entre l'altitude normal calculée à partir de la cote géopotentielle et celle dans le tableau est probablement dû à la latitude initiale prise.
'''