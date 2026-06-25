import json

with open(
    "Data/users/e3b4e7d2d797/matched_profile.json",
    "r",
    encoding="utf-8"
) as f:

    profile = json.load(f)

print()

print("Favorites")

for movie in profile[
    "favorite_movies"
]:

    print(
        movie["title"]
    )

    print(
        movie["genres"]
    )

    print(
        movie["keywords"]
    )

    print()