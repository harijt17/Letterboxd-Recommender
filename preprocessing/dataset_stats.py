import pandas as pd

df = pd.read_csv(
    "Data/processed/movies.csv",
    nrows=1
)

print(df.columns.tolist())