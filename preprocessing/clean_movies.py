import pandas as pd
from pathlib import Path

INPUT_FILE = "Data/raw/TMDB_movie_dataset_v11.csv"
OUTPUT_FILE = "Data/processed/movies.csv"

print("Loading dataset...")

df = pd.read_csv(
    INPUT_FILE,
    low_memory=False
)

print("Original rows:", len(df))

# Keep only useful columns
columns = [
    "id",
    "title",
    "vote_average",
    "vote_count",
    "release_date",
    "runtime",
    "original_language",
    "overview",
    "popularity",
    "genres",
    "production_countries",
    "keywords"
]

df = df[columns]

# Remove missing values
df = df.dropna(
    subset=[
        "title",
        "overview",
        "genres"
    ]
)

# Remove movies with very few votes
df = df[
    df["vote_count"] >= 10
]

# Remove duplicates
df = df.drop_duplicates(
    subset=["title"]
)

# Clean text columns
text_columns = [
    "overview",
    "genres",
    "keywords",
    "production_countries"
]

for col in text_columns:

    df[col] = (
        df[col]
        .astype(str)
        .str.strip()
    )

# Reset index
df = df.reset_index(
    drop=True
)

print("Processed rows:", len(df))

Path(
    "Data/processed"
).mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    f"Saved to {OUTPUT_FILE}"
)