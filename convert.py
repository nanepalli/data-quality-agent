import pandas as pd

df = pd.read_csv("data/sample.csv")
df.to_parquet("sample.parquet")

print("Parquet file created successfully!")