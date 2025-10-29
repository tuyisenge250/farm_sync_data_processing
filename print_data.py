import pandas as pd
import numpy as np
from pathlib import Path
from functools import reduce

pd.set_option('display.max_columns', 120)
DATA_DIR = Path('data')

# Load and process all data
climate_files = [
    'Huye_climate_data.csv','Kigali_climate_data.csv','Muhanga_climate_data.csv',
    'Kibungo_climate_data.csv','Musanze_climate_data.csv','Nyagatare_climate_data.csv',
    'Rubavu_climate_data.csv','Rusizi_climate_data.csv'
]

climate_dfs = {}
for f in climate_files:
    loc = f.split('_')[0].lower()
    df = pd.read_csv(DATA_DIR / f, parse_dates=['Date'], na_values=['-999.0', -999.0])
    df.replace(-999.0, np.nan, inplace=True)
    df = df.rename(columns={'T2M':'temp_c','PRECTOTCORR':'precip_mm','WS2M':'wind_m_s','RH2M':'rh_pct','ALLSKY_SFC_SW_DWN':'sw_down'})
    df['Date'] = pd.to_datetime(df['Date']).dt.normalize()
    climate_dfs[loc] = df.groupby('Date').agg({'temp_c':'mean','precip_mm':'sum','wind_m_s':'mean','rh_pct':'mean','sw_down':'mean'}).reset_index()

# Merge climate data
all_daily = [df.rename(columns=lambda c: f"{loc}_{c}" if c!='Date' else c) for loc, df in climate_dfs.items()]
climate_all = reduce(lambda a,b: a.merge(b,on='Date',how='outer'), all_daily)

temp_cols = [c for c in climate_all.columns if c.endswith('temp_c')]
precip_cols = [c for c in climate_all.columns if c.endswith('precip_mm')]
wind_cols = [c for c in climate_all.columns if c.endswith('wind_m_s')]
rh_cols = [c for c in climate_all.columns if c.endswith('rh_pct')]

climate_avg = pd.DataFrame({
    'Date': climate_all['Date'],
    'temp_c': climate_all[temp_cols].mean(axis=1),
    'precip_mm': climate_all[precip_cols].sum(axis=1),
    'wind_m_s': climate_all[wind_cols].mean(axis=1),
    'rh_pct': climate_all[rh_cols].mean(axis=1)
}).drop_duplicates(subset=['Date']).sort_values('Date').reset_index(drop=True)

# Load tomato and harvest data
tomato = pd.read_csv(DATA_DIR / 'Tomato_price.csv', parse_dates=['Date'])
tomato = tomato.rename(columns={'Date':'Date','Average':'price_avg','Market':'market','Unit':'unit','Minimum':'min_price','Maximum':'max_price'})
tomato['Date'] = pd.to_datetime(tomato['Date']).dt.normalize()
tomato['price_avg'] = pd.to_numeric(tomato['price_avg'], errors='coerce')

harvest = pd.read_csv(DATA_DIR / 'harvest_dataset.csv', parse_dates=['Date'])
harvest['Date'] = pd.to_datetime(harvest['Date']).dt.tz_localize(None).dt.normalize()
harvest_daily = harvest.groupby('Date').agg({'Harvest_kg':'sum','Price_index':'mean'}).reset_index()

# Final merge
df = tomato.merge(climate_avg, on='Date', how='left').merge(harvest_daily, on='Date', how='left')
df[['Harvest_kg','Price_index']] = df[['Harvest_kg','Price_index']].ffill().bfill()

print("Final dataset shape:", df.shape)
print("\nColumns:", list(df.columns))
print("\nFirst 5 rows:")
print(df.head())
print("\nData types:")
print(df.dtypes)
print("\nMissing values:")
print(df.isna().sum())
print("\nDate range:", df['Date'].min(), "to", df['Date'].max())