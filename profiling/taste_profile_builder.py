import json
from collections import Counter
from pathlib import Path


class TasteProfileBuilder:

    FAVORITE_WEIGHT = 3

    def process_movie(
        self,
        movie,
        weight,
        genre_counter,
        language_counter,
        keyword_counter,
        country_counter
    ):

        # Genres

        genres = movie.get(
            "genres",
            ""
        )

        for genre in str(
            genres
        ).split(","):

            genre = genre.strip()

            if genre:

                genre_counter[
                    genre
                ] += weight

        # Language

        language = movie.get(
            "language"
        )

        if language:

            language_counter[
                language
            ] += weight

        # Keywords

        keywords = movie.get(
            "keywords",
            ""
        )

        for keyword in str(
            keywords
        ).split(","):

            keyword = (
                keyword.strip()
            )

            if keyword:

                keyword_counter[
                    keyword
                ] += weight

        # Countries

        countries = movie.get(
            "production_countries",
            ""
        )

        for country in str(
            countries
        ).split(","):

            country = (
                country.strip()
            )

            if country:

                country_counter[
                    country
                ] += weight

    def build_profile(
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

        matched_movies = profile.get(
            "matched_movies",
            []
        )

        favorite_movies = profile.get(
            "favorite_movies",
            []
        )

        genre_counter = Counter()
        language_counter = Counter()
        keyword_counter = Counter()
        country_counter = Counter()

        # ----------------------
        # Regular watched movies
        # ----------------------

        for movie in matched_movies:

            self.process_movie(
                movie,
                1,
                genre_counter,
                language_counter,
                keyword_counter,
                country_counter
            )

        # ----------------------
        # Favorite movies
        # ----------------------

        for movie in favorite_movies:

            self.process_movie(
                movie,
                self.FAVORITE_WEIGHT,
                genre_counter,
                language_counter,
                keyword_counter,
                country_counter
            )

        taste_profile = {

            "total_movies":
                len(
                    matched_movies
                ),

            "favorite_movies":
                len(
                    favorite_movies
                ),

            "top_genres":
                dict(
                    genre_counter
                    .most_common(20)
                ),

            "top_languages":
                dict(
                    language_counter
                    .most_common(20)
                ),

            "top_keywords":
                dict(
                    keyword_counter
                    .most_common(50)
                ),

            "top_countries":
                dict(
                    country_counter
                    .most_common(20)
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
                taste_profile,
                f,
                indent=4,
                ensure_ascii=False
            )

        return {

            "output_file":
                str(output_file),

            "movies":
                len(
                    matched_movies
                ),

            "favorites":
                len(
                    favorite_movies
                ),

            "genres":
                len(
                    genre_counter
                ),

            "languages":
                len(
                    language_counter
                ),

            "keywords":
                len(
                    keyword_counter
                ),

            "countries":
                len(
                    country_counter
                )
        }