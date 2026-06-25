import json

import pandas as pd


class CandidateGenerator:

    def __init__(
        self,
        movie_dataset_path="Data/processed/movies.csv"
    ):

        self.movies_df = pd.read_csv(
            movie_dataset_path,
            low_memory=False
        )

    def generate_candidates(
        self,
        matched_profile_file,
        top_genres_count=5,
        top_languages_count=3
    ):

        with open(
            matched_profile_file,
            "r",
            encoding="utf-8"
        ) as f:

            profile = json.load(f)

        matched_movies = profile.get(
            "matched_movies",
            []
        )

        favorite_movies = profile.get(
            "favorite_movies",
            []
        )

        # ----------------------
        # Watched Movie IDs
        # ----------------------

        watched_ids = set()

        for movie in matched_movies:

            movie_id = movie.get(
                "movie_id"
            )

            if movie_id:

                watched_ids.add(
                    movie_id
                )

        # ----------------------
        # Build Genre Profile
        # ----------------------

        genre_counts = {}

        for movie in matched_movies:

            genres = movie.get(
                "genres",
                ""
            )

            for genre in str(
                genres
            ).split(","):

                genre = genre.strip()

                if not genre:
                    continue

                genre_counts[
                    genre
                ] = (
                    genre_counts.get(
                        genre,
                        0
                    )
                    + 1
                )

        # Favorites get 3x weight

        for movie in favorite_movies:

            genres = movie.get(
                "genres",
                ""
            )

            for genre in str(
                genres
            ).split(","):

                genre = genre.strip()

                if not genre:
                    continue

                genre_counts[
                    genre
                ] = (
                    genre_counts.get(
                        genre,
                        0
                    )
                    + 3
                )

        # ----------------------
        # Build Language Profile
        # ----------------------

        language_counts = {}

        for movie in matched_movies:

            language = movie.get(
                "language"
            )

            if not language:
                continue

            language_counts[
                language
            ] = (
                language_counts.get(
                    language,
                    0
                )
                + 1
            )

        for movie in favorite_movies:

            language = movie.get(
                "language"
            )

            if not language:
                continue

            language_counts[
                language
            ] = (
                language_counts.get(
                    language,
                    0
                )
                + 3
            )

        # ----------------------
        # Top Genres
        # ----------------------

        top_genres = [

            genre

            for genre, _ in sorted(
                genre_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:top_genres_count]
        ]

        # ----------------------
        # Top Languages
        # ----------------------

        top_languages = [

            language

            for language, _ in sorted(
                language_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:top_languages_count]
        ]

        # ----------------------
        # Candidate Filtering
        # ----------------------

        candidates = []

        for _, row in (
            self.movies_df.iterrows()
        ):

            movie_id = row["id"]

            # Skip watched

            if movie_id in watched_ids:
                continue

            # Language filter

            language = row.get(
                "original_language"
            )

            if (
                language
                not in top_languages
            ):
                continue

            # Genre filter

            genres = str(
                row.get(
                    "genres",
                    ""
                )
            )

            genre_matches = 0

            for genre in top_genres:

                if genre in genres:

                    genre_matches += 1

            # Require at least 2 matching genres

            if genre_matches < 2:
                continue

            release_date = row.get(
                "release_date"
            )

            year = ""

            if pd.notna(
                release_date
            ):

                year = str(
                    release_date
                ).split("-")[0]

            display_title = (
                f"{row['title']} ({year})"
                if year
                else row["title"]
            )

            candidates.append({

                "movie_id":
                    int(row["id"]),

                "title":
                    row["title"],

                "display_title":
                    display_title,

                "release_date":
                    release_date,

                "genres":
                    row.get(
                        "genres"
                    ),

                "keywords":
                    row.get(
                        "keywords"
                    ),

                "overview":
                    row.get(
                        "overview"
                    ),

                "language":
                    row.get(
                        "original_language"
                    ),

                "vote_average":
                    row.get(
                        "vote_average"
                    ),

                "vote_count":
                    row.get(
                        "vote_count"
                    ),

                "popularity":
                    row.get(
                        "popularity"
                    )
            })

        return {

            "candidate_count":
                len(candidates),

            "top_genres":
                top_genres,

            "top_languages":
                top_languages,

            "candidates":
                candidates
        }