import json

from matching.movie_matcher import (
    MovieMatcher
)


class FavoriteExtractor:

    def __init__(self):

        self.matcher = (
            MovieMatcher()
        )

    def enrich_favorites(
        self,
        favorites
    ):

        enriched = []

        for title in favorites:

            movie = (
                self.matcher
                .enrich_movie(title)
            )

            if movie:

                enriched.append(
                    movie
                )

        return enriched