import json
from pathlib import Path

from .movie_matcher import MovieMatcher
from profiling.favorite_extractor import (
    FavoriteExtractor
)


class ProfileEnricher:

    def __init__(
        self,
        movie_dataset_path=None
    ):

        self.matcher = MovieMatcher(
            movie_dataset_path
        )

        self.favorite_extractor = (
            FavoriteExtractor()
        )

    def enrich_profile(
        self,
        input_file,
        output_file
    ):

        with open(
            input_file,
            "r",
            encoding="utf-8"
        ) as f:

            profile = json.load(f)

        matched_movies = []
        future_movies = []
        unmatched_movies = []

        watched = profile.get(
            "watched",
            []
        )

        for movie in watched:

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

            except (
                TypeError,
                ValueError
            ):
                year = None

            if (
                year is not None
                and year > 2024
            ):

                future_movies.append({

                    "title":
                        title,

                    "year":
                        year
                })

                continue

            result = (
                self.matcher
                .enrich_movie(
                    title
                )
            )

            if result:

                result["year"] = year

                matched_movies.append(
                    result
                )

            else:

                unmatched_movies.append({

                    "title":
                        title,

                    "year":
                        year
                })

        # -------------------------
        # Favorites
        # -------------------------

        favorites = profile.get(
            "favorites",
            []
        )

        favorite_movies = (
            self.favorite_extractor
            .enrich_favorites(
                favorites
            )
        )

        enriched = {

            "profile":
                profile.get(
                    "profile",
                    {}
                ),

            "profile_stats":
                profile.get(
                    "profile_stats",
                    {}
                ),

            "favorites":
                favorites,

            "favorite_movies":
                favorite_movies,

            "matched_movies":
                matched_movies,

            "future_movies":
                future_movies,

            "unmatched_movies":
                unmatched_movies,

            "ratings":
                profile.get(
                    "ratings",
                    []
                ),

            "reviews":
                profile.get(
                    "reviews",
                    []
                ),

            "diary":
                profile.get(
                    "diary",
                    []
                )
        }

        output_file = Path(
            output_file
        )

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                enriched,
                f,
                indent=4,
                ensure_ascii=False,
                default=str
            )

        return {

            "output_file":
                str(output_file),

            "matched":
                len(
                    matched_movies
                ),

            "future":
                len(
                    future_movies
                ),

            "unmatched":
                len(
                    unmatched_movies
                ),

            "favorites":
                len(
                    favorite_movies
                ),

            "match_rate":
                round(
                    (
                        len(
                            matched_movies
                        )
                        /
                        max(
                            1,
                            len(
                                matched_movies
                            )
                            +
                            len(
                                unmatched_movies
                            )
                        )
                    )
                    * 100,
                    2
                )
        }