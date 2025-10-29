import pandas as pd
from pathlib import Path

DATA_DIR = Path('data')
tomato = pd.read_csv(DATA_DIR / 'Tomato_price.csv', parse_dates=['Date'])
print("Tomato columns:", tomato.columns.tolist())
print("First few rows:")
print(tomato.head())