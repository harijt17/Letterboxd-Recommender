import json


class RankingEngine:

    GENRE_WEIGHT = 25
    KEYWORD_WEIGHT = 25
    FAVORITE_WEIGHT = 30
    LANGUAGE_WEIGHT = 10
    QUALITY_WEIGHT = 10

    def __init__(self):
        pass

    def _split_values(
        self,
        value
    ):

        if not value:
            return set()

        return {

            item.strip().lower()

            for item in str(
                value
            ).split(",")

            if item.strip()
        }

    def _build_user_profile(
        self,
        matched_profile
    ):

        matched_movies = matched_profile.get(
            "matched_movies",
            []
        )

        favorite_movies = matched_profile.get(
            "favorite_movies",
            []
        )

        genres = set()
        keyword_weights = {}
        languages = set()

        # ----------------------
        # Watched Movies
        # ----------------------

        for movie in matched_movies:

            genres.update(
                self._split_values(
                    movie.get(
                        "genres"
                    )
                )
            )

            for keyword in self._split_values(
                movie.get(
                    "keywords"
                )
            ):

                keyword_weights[
                    keyword
                ] = (
                    keyword_weights.get(
                        keyword,
                        0
                    )
                    + 1
                )

            language = movie.get(
                "language"
            )

            if language:

                languages.add(
                    str(
                        language
                    ).lower()
                )

        # ----------------------
        # Favorites
        # ----------------------

        for movie in favorite_movies:

            genres.update(
                self._split_values(
                    movie.get(
                        "genres"
                    )
                )
            )

            for keyword in self._split_values(
                movie.get(
                    "keywords"
                )
            ):

                keyword_weights[
                    keyword
                ] = (
                    keyword_weights.get(
                        keyword,
                        0
                    )
                    + 5
                )

        return {

            "genres":
                genres,

            "keyword_weights":
                keyword_weights,

            "languages":
                languages,

            "favorite_movies":
                favorite_movies
        }

    def _genre_score(
        self,
        candidate_genres,
        user_genres
    ):

        if not candidate_genres:
            return 0

        overlap = len(
            candidate_genres
            &
            user_genres
        )

        return min(
            100,
            overlap * 20
        )

    def _keyword_score(
        self,
        candidate_keywords,
        keyword_weights
    ):

        if not candidate_keywords:
            return 0

        score = 0

        for keyword in candidate_keywords:

            score += (
                keyword_weights.get(
                    keyword,
                    0
                )
            )

        return min(
            100,
            score
        )

    def _favorite_score(
        self,
        candidate,
        favorite_movies
    ):

        score = 0

        candidate_genres = (
            self._split_values(
                candidate.get(
                    "genres"
                )
            )
        )

        candidate_keywords = (
            self._split_values(
                candidate.get(
                    "keywords"
                )
            )
        )

        for favorite in favorite_movies:

            favorite_genres = (
                self._split_values(
                    favorite.get(
                        "genres"
                    )
                )
            )

            favorite_keywords = (
                self._split_values(
                    favorite.get(
                        "keywords"
                    )
                )
            )

            genre_overlap = len(
                candidate_genres
                &
                favorite_genres
            )

            keyword_overlap = len(
                candidate_keywords
                &
                favorite_keywords
            )

            score += (
                genre_overlap * 5
            )

            score += (
                keyword_overlap * 2
            )

        return min(
            100,
            score
        )

    def _language_score(
        self,
        candidate_language,
        user_languages
    ):

        if (
            str(
                candidate_language
            ).lower()
            in user_languages
        ):

            return 100

        return 0

    def _quality_score(
        self,
        vote_average,
        vote_count
    ):

        try:

            vote_average = float(
                vote_average
            )

        except:

            vote_average = 0

        try:

            vote_count = float(
                vote_count
            )

        except:

            vote_count = 0

        rating_component = (
            vote_average / 10
        ) * 70

        popularity_component = min(
            30,
            vote_count / 1000 * 30
        )

        return (
            rating_component
            +
            popularity_component
        )

    def rank(
        self,
        matched_profile_file,
        candidates
    ):

        with open(
            matched_profile_file,
            "r",
            encoding="utf-8"
        ) as f:

            matched_profile = json.load(
                f
            )

        user_profile = (
            self._build_user_profile(
                matched_profile
            )
        )

        ranked_movies = []

        for candidate in candidates:

            candidate_genres = (
                self._split_values(
                    candidate.get(
                        "genres"
                    )
                )
            )

            candidate_keywords = (
                self._split_values(
                    candidate.get(
                        "keywords"
                    )
                )
            )

            genre_score = (
                self._genre_score(
                    candidate_genres,
                    user_profile[
                        "genres"
                    ]
                )
            )

            keyword_score = (
                self._keyword_score(
                    candidate_keywords,
                    user_profile[
                        "keyword_weights"
                    ]
                )
            )

            favorite_score = (
                self._favorite_score(
                    candidate,
                    user_profile[
                        "favorite_movies"
                    ]
                )
            )

            language_score = (
                self._language_score(
                    candidate.get(
                        "language"
                    ),
                    user_profile[
                        "languages"
                    ]
                )
            )

            quality_score = (
                self._quality_score(
                    candidate.get(
                        "vote_average"
                    ),
                    candidate.get(
                        "vote_count"
                    )
                )
            )

            final_score = (

                genre_score
                * self.GENRE_WEIGHT

                +

                keyword_score
                * self.KEYWORD_WEIGHT

                +

                favorite_score
                * self.FAVORITE_WEIGHT

                +

                language_score
                * self.LANGUAGE_WEIGHT

                +

                quality_score
                * self.QUALITY_WEIGHT

            ) / 100

            candidate[
                "score"
            ] = round(
                final_score,
                2
            )

            ranked_movies.append(
                candidate
            )

        ranked_movies.sort(
            key=lambda x: x[
                "score"
            ],
            reverse=True
        )

        return ranked_movies