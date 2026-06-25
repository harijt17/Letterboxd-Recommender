import json
import pandas as pd

with open(
    "Data/users/harijt17.json",
    "r",
    encoding="utf-8"
) as f:
    profile = json.load(f)

watched = profile["watched"]

before_2025 = 0
after_2024 = 0

for movie in watched:

    year = (
        movie.get("Year")
        or movie.get("year")
    )

    try:
        year = int(year)

        if year <= 2024:
            before_2025 += 1
        else:
            after_2024 += 1

    except:
        pass

print(f"Total watched: {len(watched)}")
print(f"Movies up to 2024: {before_2025}")
print(f"Movies after 2024: {after_2024}")