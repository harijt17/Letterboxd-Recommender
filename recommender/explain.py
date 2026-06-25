class RecommendationExplainer:

    def __init__(self):
        pass

    def _split_values(
        self,
        value
    ):

        if not value:
            return set()

        return {

            item.strip()

            for item in str(
                value
            ).split(",")

            if item.strip()
        }

    def explain(
        self,
        movie,
        top_genres,
        top_keywords=None
    ):

        movie_genres = (
            self._split_values(
                movie.get(
                    "genres"
                )
            )
        )

        matched_genres = []

        for genre in top_genres:

            if genre in movie_genres:

                matched_genres.append(
                    genre
                )

        matched_genres = (
            matched_genres[:3]
        )

        if matched_genres:

            return (
                "Matches your interest in "
                +
                ", ".join(
                    matched_genres
                )
                +
                "."
            )

        return (
            "Recommended based on "
            "your viewing history."
        )