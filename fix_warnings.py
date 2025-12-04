# Fix for pandas deprecation warnings and errors

# Replace deprecated fillna(method='bfill') with bfill()
data['Lag_1d'] = data['Price'].shift(1).bfill()
data['Lag_7d'] = data['Price'].shift(7).bfill()
data['Lag_30d'] = data['Price'].shift(30).bfill()

# Replace deprecated fillna(method='bfill') with bfill()
data['Rolling_Mean_7d'] = data['Price'].rolling(7).mean().bfill()

# Fix seaborn barplot - assign hue parameter
sns.barplot(x=price_corr.index, y=price_corr.values, hue=price_corr.index, palette="viridis", legend=False)

# Fix datetime accessor error - ensure column is datetime
df["date"] = pd.to_datetime(df["date"])
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["week_number"] = df["date"].dt.isocalendar().week