# Step 6 — clean & merge harvest_dataset
harvest['Date'] = pd.to_datetime(harvest['Date']).dt.tz_localize(None).dt.normalize()
harvest_daily = harvest.groupby('Date').agg({'Harvest_kg':'sum','Price_index':'mean'}).reset_index()

df = df.merge(harvest_daily, on='Date', how='left')
df[['Harvest_kg','Price_index']] = df[['Harvest_kg','Price_index']].ffill().bfill()
print("After harvest merge, missing values:\n", df.isna().sum())
print("\nFinal dataset shape:", df.shape)
print("\nColumns:", list(df.columns))
print("\nFirst 5 rows:")
print(df.head())