from movie_matcher import MovieMatcher


matcher = MovieMatcher()

test_movies = [

    "Inception",

    "Interstellar",

    "Cinema Paradiso",

    "Thalapathi",

    "Meiyazhagan",

    "Vaaranam Aayiram"
]

for title in test_movies:

    result = matcher.enrich_movie(
        title
    )

    print("\n" + "=" * 50)

    print(
        f"Query: {title}"
    )

    if result:

        print(
            f"Matched: "
            f"{result['title']}"
        )

        print(
            f"Genres: "
            f"{result['genres']}"
        )

    else:

        print(
            "No match found"
        )