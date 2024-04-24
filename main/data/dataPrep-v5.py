# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 11:21:08 2022

@author: matta
"""

import pandas as pd
import geopandas as gpd
import hashlib

def hash_names(row):
    name = row.full_name + ' ' + row.party
    return hashlib.sha256(name.encode()).hexdigest()

print('Reading data')

#%% Prep party candidates
df_mca = pd.read_csv('Ward_Final.csv', usecols=['County Name', 'County Code',
                                                  'Constituency Name', 'Constituency Code', 
                                                  'Ward Name', 'Ward Code',
                                                  'Surname', 'Other Names', 
                                                  'Political Party Name'])

df_mca = df_mca[['County Name', 'County Code', 'Constituency Name', 
                 'Constituency Code', 'Ward Name', 'Ward Code', 'Surname',
                 'Other Names', 'Political Party Name']]

df_mca.columns = ['county_name', 'county_code', 'constituency_name', 'constituency_code',
                  'ward_name', 'ward_code', 'surname', 'other_names', 'party']

df_mca.ward_name = df_mca.ward_name.str.replace('\r', ' ').apply(lambda x: ' '.join(x.split()))
df_mca.ward_name = df_mca.ward_name.str.title()

df_mca.party = df_mca.party.str.replace('\n|-', ' ').apply(lambda x: ' '.join(x.split()))

df_mca.county_name = df_mca.county_name.str.replace('-', ' ').apply(lambda x: ' '.join(x.split())).str.title()

df_mca.constituency_name = df_mca.constituency_name.str.replace('\r', ' ').apply(lambda x: ' '.join(x.split())).str.title()

df_mca.other_names = df_mca.other_names.str.replace('\r', ' ').apply(lambda x: ' '.join(x.split()))
df_mca.other_names = df_mca.other_names.str.replace('` ', '\'')
df_mca['full_name'] = df_mca.apply(lambda x: x.other_names + ' ' +  x.surname, axis=1)
   
df_mca.drop_duplicates(inplace=True)
df_mca['code'] = 'WA'

df_mca['id_number'] = df_mca.apply(lambda x: hash_names(x), axis=1)
#%% Prep Parliament Candidates
df_mpi = pd.read_csv('NationalAssembly_Final.csv', usecols=['County Name', 'County Code', 
                                                 'Constituency Name', 'Constituency Code', 
                                                 'Surname', 'Other Names', 'Political Party Name'])

df_mpi = df_mpi[['County Name', 'County Code', 'Constituency Name', 
                 'Constituency Code', 'Surname', 'Other Names', 
                 'Political Party Name']]

df_mpi.columns = ['county_name', 'county_code', 'constituency_name', 'constituency_code',
                  'surname', 'other_names', 'party']

df_mpi.party = df_mpi.party.str.replace('\n|-', ' ').apply(lambda x: ' '.join(x.split()))

df_mpi.county_name = df_mpi.county_name.str.replace('-', ' ').apply(lambda x: ' '.join(x.split()))

df_mpi.constituency_name = df_mpi.constituency_name.str.replace('\r', ' ').apply(lambda x: ' '.join(x.split()))

df_mpi.other_names = df_mpi.other_names.str.replace('\r', ' ').apply(lambda x: ' '.join(x.split()))
df_mpi.other_names = df_mpi.other_names.str.replace('` ', '\'')
df_mpi['full_name'] = df_mpi.apply(lambda x: x.other_names + ' ' +  x.surname, axis=1)

df_mpi.drop_duplicates(inplace=True)
df_mpi['code'] = 'MP'

df_mpi['id_number'] = df_mpi.apply(lambda x: hash_names(x), axis=1)
#%% Prep Governor Candidates
df_mpg = pd.read_csv('CountyGovernor_Final.csv',
                     usecols=['County Name', 'County Code', 'Surname', 'Other Names', 'Political Party Name'])

df_mpg = df_mpg[['County Name', 'County Code', 'Surname', 'Other Names', 'Political Party Name']]

df_mpg.columns = ['county_name', 'county_code', 'surname', 'other_names', 'party']

df_mpg.party = df_mpg.party.str.replace('\n|-', ' ').apply(lambda x: ' '.join(x.split()))

df_mpg.county_name = df_mpg.county_name.str.replace('-', ' ').apply(lambda x: ' '.join(x.split()))

df_mpg.other_names = df_mpg.other_names.str.replace('\r', ' ').apply(lambda x: ' '.join(x.split()))
df_mpg.other_names = df_mpg.other_names.str.replace('` ', '\'')
df_mpg['full_name'] = df_mpg.apply(lambda x: x.other_names + ' ' +  x.surname, axis=1)
   
df_mpg.drop_duplicates(inplace=True)
df_mpg['code'] = 'GV'

df_mpg['id_number'] = df_mpg.apply(lambda x: hash_names(x), axis=1)
#%% Prep Senators
df_sen = pd.read_csv('Senate_Final.csv', usecols=['County Name', 'County Code', 'Surname',
                                                      'Other Names', 'Political Party Name'])

df_sen = df_sen[['County Name', 'County Code', 'Surname','Other Names', 'Political Party Name']]

df_sen.columns = ['county_name', 'county_code', 'surname', 'other_names', 'party']

df_sen.party = df_sen.party.str.replace('\n|-', ' ').apply(lambda x: ' '.join(x.split()))

df_sen.county_name = df_sen.county_name.str.replace('-', ' ').apply(lambda x: ' '.join(x.split()))

df_sen.other_names = df_sen.other_names.str.replace('\r', ' ').apply(lambda x: ' '.join(x.split()))
df_sen.other_names = df_sen.other_names.str.replace('` ', '\'')
df_sen['full_name'] = df_sen.apply(lambda x: x.other_names + ' ' +  x.surname, axis=1)
   
df_sen.drop_duplicates(inplace=True)
df_sen['code'] = 'SN'

sens = [df_sen]

df_sen['id_number'] = df_sen.apply(lambda x: hash_names(x), axis=1)
#%%Prep Womxn Candidates
df_wxn = pd.read_csv('Women_Final.csv',
                     usecols=['County Name', 'County Code', 'Surname', 'Other Names', 'Political Party Name'])

df_wxn = df_wxn[['County Name', 'County Code', 'Surname', 'Other Names', 'Political Party Name']]

df_wxn.columns = ['county_name', 'county_code', 'surname', 'other_names', 'party']

df_wxn.party = df_wxn.party.str.replace('\n|-', ' ').apply(lambda x: ' '.join(x.split()))

df_wxn.county_name = df_wxn.county_name.str.replace('-', ' ').apply(lambda x: ' '.join(x.split()))

df_wxn.other_names = df_wxn.other_names.str.replace('\r', ' ').apply(lambda x: ' '.join(x.split()))
df_wxn.other_names = df_wxn.other_names.str.replace('` ', '\'')
df_wxn['full_name'] = df_wxn.apply(lambda x: x.other_names + ' ' +  x.surname, axis=1)
   
df_wxn.drop_duplicates(inplace=True)
df_wxn['code'] = 'WM'

wxns = [df_wxn]

df_wxn['id_number'] = df_wxn.apply(lambda x: hash_names(x), axis=1)
#%% Prep Wards
df_w = gpd.read_file('kenya_wards/kenya_wards.shp')[['county', 'ward', 'geometry']]
df_w.columns = ['county_name', 'ward_name', 'geometry']
df_w.county_name = df_w.county_name.str.title()
df_w.county_name = df_w.county_name.str.replace('-', ' ').apply(lambda x: ' '.join(x.split()))
df_w.ward_name = df_w.ward_name.str.title()
df_w.ward_name = df_w.ward_name.str.replace('Ward', '').apply(lambda x: ' '.join(x.split()))
df_w.ward_name = df_w.ward_name.str.replace('/', ' ')

#%%
index_df = df_mca[['county_code', 'constituency_code', 'ward_code']].drop_duplicates()

mpi_joined = pd.merge(index_df, df_mpi, on=['county_code', 'constituency_code'], how='inner').drop_duplicates(subset=['id_number', 'ward_code'])

mpg_joined = pd.merge(index_df, df_mpg, on=['county_code'], how='inner').drop_duplicates(subset=['id_number', 'ward_code'])

sen_joined = pd.merge(index_df, df_sen, on=['county_code'], how='inner').drop_duplicates(subset=['id_number', 'ward_code'])

wxn_joined = pd.merge(index_df, df_wxn, on=['county_code'], how='inner').drop_duplicates(subset=['id_number', 'ward_code'])

full_set = pd.concat([df_mca, mpi_joined, mpg_joined, sen_joined, wxn_joined], axis=0)

full_set = full_set.drop(['constituency_name', 'ward_name'], axis=1)

full_set = pd.merge(full_set, df_mca[['constituency_code', 'constituency_name', 'ward_code', 'ward_name']].drop_duplicates(), on=['constituency_code', 'ward_code'], how='left')

full_set.county_name = full_set.county_name.str.title()
full_set.constituency_name = full_set.constituency_name.str.title()
full_set.ward_name = full_set.ward_name.str.title()
full_set.party = full_set.party.str.title()
full_set.full_name = full_set.full_name.str.title()
full_set = full_set.sort_values(['code', 'county_name', 'constituency_name', 'ward_name', 'party'])
full_set.to_excel('Full_Set_NoPres-v8.xlsx', index=False)

#%%
# df_out = pd.merge(full_set, df_w, on='ward_name')
# df_out = gpd.GeoDataFrame(df_out, geometry='geometry')
# df_out.to_file('gdf_mca_wards_v2.geojson', driver='GeoJSON')

#%%
# pd.Series(full_set[~full_set.ward_name.isin(df_w.ward_name)].ward_name.sort_values().unique()).to_csv('missing_wards.csv', index=False)