from recommender.candidate_generator import (
    CandidateGenerator
)

from recommender.ranking_engine import (
    RankingEngine
)

from recommender.explain import (
    RecommendationExplainer
)


class Recommender:

    def __init__(self):

        self.candidate_generator = (
            CandidateGenerator()
        )

        self.ranking_engine = (
            RankingEngine()
        )

        self.explainer = (
            RecommendationExplainer()
        )

    def recommend(
        self,
        matched_profile_file,
        limit=50
    ):

        candidate_result = (
            self.candidate_generator
            .generate_candidates(
                matched_profile_file
            )
        )

        candidates = (
            candidate_result[
                "candidates"
            ]
        )

        ranked_movies = (
            self.ranking_engine
            .rank(
                matched_profile_file,
                candidates
            )
        )

        recommendations = (
            ranked_movies[:limit]
        )

        top_genres = (
            candidate_result[
                "top_genres"
            ]
        )

        for movie in recommendations:

            movie[
                "reason"
            ] = (
                self.explainer
                .explain(
                    movie,
                    top_genres
                )
            )

        return {

            "candidate_count":
                candidate_result[
                    "candidate_count"
                ],

            "top_genres":
                candidate_result[
                    "top_genres"
                ],

            "top_languages":
                candidate_result[
                    "top_languages"
                ],

            "recommendations":
                recommendations
        }