import json
from movie_matcher import MovieMatcher

matcher = MovieMatcher()

with open(
    "Data/users/harijt17.json",
    "r",
    encoding="utf-8"
) as f:
    profile = json.load(f)

failed = []

for movie in profile["watched"]:

    title = (
        movie.get("Name")
        or movie.get("Title")
        or movie.get("title")
    )

    year = (
        movie.get("Year")
        or movie.get("year")
    )

    try:
        year = int(year)
    except:
        year = None

    # Skip future movies
    if year and year > 2024:
        continue

    result = matcher.match_movie(title)

    if result is None:
        failed.append(
            {
                "title": title,
                "year": year
            }
        )

print("\nUnmatched movies:\n")

for movie in failed[:50]:
    print(
        f"{movie['title']} "
        f"({movie['year']})"
    )

print(
    f"\nTotal unmatched: "
    f"{len(failed)}"
)

total_watched = len(profile["watched"])

eligible_movies = 0

for movie in profile["watched"]:

    year = (
        movie.get("Year")
        or movie.get("year")
    )

    try:
        year = int(year)

        if year <= 2024:
            eligible_movies += 1

    except:
        pass

matched = eligible_movies - len(failed)

match_rate = (
    matched / eligible_movies
) * 100

print("\n" + "=" * 50)

print(
    f"Total Watched: "
    f"{total_watched}"
)

print(
    f"Eligible Movies (<=2024): "
    f"{eligible_movies}"
)

print(
    f"Matched: "
    f"{matched}"
)

print(
    f"Unmatched: "
    f"{len(failed)}"
)

print(
    f"Match Rate: "
    f"{match_rate:.2f}%"
)