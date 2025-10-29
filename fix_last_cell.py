# Save processed data
augmented_df.to_csv(OUT_DIR / 'processed_farmer_data.csv', index=False)
print(f"Processed data saved to {OUT_DIR / 'processed_farmer_data.csv'}")
print("\nFinal dataset summary:")
print(augmented_df.info())
print("\nFirst 5 rows:")
print(augmented_df.head())