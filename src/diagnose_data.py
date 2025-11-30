import pandas as pd

print("=== FIXING HEADERS ===")
home_path = "data/metrica/data/Sample_Game_1/Sample_Game_1_RawTrackingData_Home_Team.csv"

# Skip first 8 rows (metadata), read headers from row 8
df = pd.read_csv(home_path, skiprows=8, low_memory=False)

print("✅ Headers after skipping metadata:")
print("Columns:", list(df.columns[:20]))
print("\nFirst 3 rows:")
print(df.head(3))

print("\nShape:", df.shape)
print("Sample data:")
print(df.iloc[10:15, :5])  # Rows 10-15, first 5 columns
