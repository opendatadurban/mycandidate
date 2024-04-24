# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 11:09:36 2022

@author: matta
"""

import pandas as pd
import geopandas as gpd
from sqlalchemy.engine import create_engine

print('reading gis...')
df_w = gpd.read_file('kenya_wards/kenya_wards.shp')[['county', 'ward', 'geometry']]
df_w.columns = ['county_name', 'ward_name', 'geometry']
df_w.county_name = df_w.county_name.str.title()
df_w.county_name = df_w.county_name.str.replace('-', ' ').apply(lambda x: ' '.join(x.split()))
df_w.ward_name = df_w.ward_name.str.title()
df_w.ward_name = df_w.ward_name.str.replace('Ward', '').apply(lambda x: ' '.join(x.split()))
df_w.ward_name = df_w.ward_name.str.replace('/', ' ')
df_w = gpd.GeoDataFrame(df_w, geometry='geometry')

df_reps = pd.read_csv('mispelled_wards.csv')

df_reps.IEBC = df_reps.IEBC.str.replace('\r', ' ').apply(lambda x: ' '.join(x.split()))
df_reps.IEBC = df_reps.IEBC.str.title()

replace = {}

for i, row in df_reps.iterrows():
    replace[row.Geo] = row.IEBC

df_w.ward_name = df_w.ward_name.replace(replace)

df_w.county_name = df_w.county_name.replace({'Nairobi': 'Nairobi City',
                                             'Muranga': "Murang'A"})

#%%

# #LOCAL
# db = create_engine("postgresql://my_candidate_kenya:my_candidate_kenya@localhost/my_candidate_kenya")
# #PRODUCTION
# #STAGING

# conn = db.connect()

# print('writing gis...')
# df_w.to_postgis('wards', con=conn, if_exists='replace')

# print('reading tabular...')
# df_c = pd.read_excel('Full_Set_NoPres-v8.xlsx')
# df_c = df_c.drop(['county_code', 'constituency_code', 'ward_code'], axis=1)
# df_c.ward_name = df_c.ward_name.replace({'Township.': 'Township'})
# print('writing tabular...')
# df_c.to_sql('candidates', con=conn, index=False, if_exists='replace')

# conn.close()
# db.dispose()
    