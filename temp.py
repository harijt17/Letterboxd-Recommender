from recommender.recommend import (
    Recommender
)

recommender = (
    Recommender()
)

result = recommender.recommend(
    "Data/users/e3b4e7d2d797/matched_profile.json",
    limit=10
)

for movie in result[
    "recommendations"
]:

    print()

    print(
        movie["title"]
    )

    print(
        "Score:",
        movie["score"]
    )

    print(
        movie["reason"]
    )