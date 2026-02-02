import sys
import pandas as pd

print("arguments:", sys.argv)

month = int(sys.argv[1])

df = pd.DataFrame({
    "day": [1, 2],
    "num_passengers": [3, 4],
})
df["month"] = month
print(df)

output_file = f"output_month_{month}.parquet"
df.to_parquet(output_file)

print(f"Saved result to {output_file}")
print(f"hello pipeline, month = {month}")