import pandas as pd
import numpy as np

df_raw = pd.read_csv('https://raw.githubusercontent.com/minhealthnz/nz-covid-data/main/vaccine-data/sa2-data/uptake_sa2_dhb_latest.csv')

df = df_raw.copy()

# clean up ambiguous MoH data
for col in df.columns:
    df[col] = df[col].str.replace('<','')
    df[col] = df[col].str.replace('>','')
    df[col] = df[col].str.replace(' or less','')
    df[col] = df[col].str.replace('masked', '0')

# convert columns to numeric
for col in ['dose1_cnt', 'dose2_cnt', 'pop_cnt',
       'dose1_uptake', 'dose2_uptake']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# create buckets for vaccine uptake
for col in range(1,3):
    df['dose{}_uptake_bucket'.format(col)] = np.where(
        df['dose{}_uptake'.format(col)] < 50,
        25,
        df['dose{}_uptake'.format(col)])
    for i in range(0,1000,50):
        df['dose{}_uptake_bucket'.format(col)] = np.where(
            (df['dose{}_uptake'.format(col)] >= i) & (df['dose{}_uptake'.format(col)] < i+50),
            i+25,
            df['dose{}_uptake_bucket'.format(col)])

# compute percentage window of uptake
for col in range(1,3):
    df['dose{}_uptake_bucket_perc'.format(col)] = df['dose{}_uptake_bucket'.format(col)]/10
    df['dose{}_uptake_bucket_perc'.format(col)] = df['dose{}_uptake_bucket_perc'.format(col)].astype(float)

# rename columns for easier ingestion into the viz
for i in range(0,2):
    df.rename(columns={
        'dose{}_uptake_bucket_perc'.format(i+1):'dose{}_uptake_perc'.format(i+1)}, inplace=True)

# save to csv
df[['sa2_code', 'sa2_name', 'dhb', 
    'dose1_uptake_perc', 'dose2_uptake_perc']].to_csv('suburb_data.csv', index=False)