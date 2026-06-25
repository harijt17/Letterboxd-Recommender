from pathlib import Path
import re

import pandas as pd
from rapidfuzz import process, fuzz


DEFAULT_DATASET = (
    Path("Data")
    / "processed"
    / "movies.csv"
)


def to_python(value):

    if pd.isna(value):
        return None

    if hasattr(value, "item"):
        return value.item()

    return value

def normalize_title(title):

    title = str(title).lower()

    title = title.replace("&", "and")

    title = title.replace("–", "-")
    title = title.replace("—", "-")

    # Remove year
    title = re.sub(
        r"\(\d{4}\)",
        "",
        title
    )

    # Remove punctuation
    title = re.sub(
        r"[^\w\s]",
        " ",
        title
    )

    # Remove extra spaces
    title = " ".join(
        title.split()
    )

    return title


def safe_value(value):

    if pd.isna(value):
        return None

    return value


class MovieMatcher:

    def __init__(
        self,
        movie_dataset_path=None
    ):

        if movie_dataset_path is None:
            movie_dataset_path = (
                DEFAULT_DATASET
            )

        self.movies_df = pd.read_csv(
            movie_dataset_path,
            low_memory=False
        )

        self.movies_df[
            "title_lower"
        ] = (
            self.movies_df["title"]
            .apply(normalize_title)
        )

        self.movie_count = len(
            self.movies_df
        )

        self.title_lookup = {

            title: idx

            for idx, title in enumerate(
                self.movies_df[
                    "title_lower"
                ]
            )
        }

        self.movie_titles = (
            self.movies_df[
                "title_lower"
            ]
            .tolist()
        )

    def exact_match(
        self,
        title
    ):

        title = normalize_title(
            title
        )

        idx = self.title_lookup.get(
            title
        )

        if idx is None:
            return None

        return (
            self.movies_df
            .iloc[idx]
        )

    def fuzzy_match(
        self,
        title,
        threshold=90
    ):

        title = normalize_title(
            title
        )

        result = process.extractOne(
            title,
            self.movie_titles,
            scorer=fuzz.WRatio
        )

        if result is None:
            return None

        match_title, score, _ = result

        if score < threshold:
            return None

        movie = self.movies_df[
            self.movies_df[
                "title_lower"
            ]
            == match_title
        ]

        if len(movie) == 0:
            return None

        return movie.iloc[0]

    def match_movie(
        self,
        title
    ):

        movie = self.exact_match(
            title
        )

        if movie is not None:
            return movie

        return self.fuzzy_match(
            title
        )

    def enrich_movie(
        self,
        title,
        rating=None
    ):

        movie = self.match_movie(
            title
        )

        if movie is None:
            return None

        return {

            "movie_id":
                int(movie["id"]),

            "title":
                to_python(
                    movie.get("title")
                ),

            "rating":
                rating,

            "genres":
                to_python(
                    movie.get("genres")
                ),

            "overview":
                to_python(
                    movie.get("overview")
                ),

            "keywords":
                to_python(
                    movie.get("keywords")
                ),

            "language":
                to_python(
                    movie.get(
                        "original_language"
                    )
                ),

            "production_countries":
                to_python(
                    movie.get(
                        "production_countries"
                    )
                ),

            "release_date":
                to_python(
                    movie.get(
                        "release_date"
                    )
                ),

            "runtime":
                to_python(
                    movie.get(
                        "runtime"
                    )
                ),

            "vote_count":
                (
                    int(
                        movie.get(
                            "vote_count"
                        )
                    )
                    if pd.notna(
                        movie.get(
                            "vote_count"
                        )
                    )
                    else None
                ),

            "popularity":
                (
                    float(
                        movie.get(
                            "popularity"
                        )
                    )
                    if pd.notna(
                        movie.get(
                            "popularity"
                        )
                    )
                    else None
                ),

            "vote_average":
                (
                    float(
                        movie.get(
                            "vote_average"
                        )
                    )
                    if pd.notna(
                        movie.get(
                            "vote_average"
                        )
                    )
                    else None
                )
        }