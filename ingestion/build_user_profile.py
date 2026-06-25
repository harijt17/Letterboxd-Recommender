import json
from pathlib import Path

from .parse_profile import parse_profile
from .parse_watched import parse_watched
from .parse_ratings import parse_ratings
from .parse_reviews import parse_reviews
from .parse_diary import parse_diary


def build_profile(
    export_folder
):

    export_folder = Path(
        export_folder
    )

    profile_data = parse_profile(
        export_folder / "profile.csv"
    )

    watched = parse_watched(
        export_folder / "watched.csv"
    )

    ratings = parse_ratings(
        export_folder / "ratings.csv"
    )

    reviews = parse_reviews(
        export_folder / "reviews.csv"
    )

    diary = parse_diary(
        export_folder / "diary.csv"
    )

    return {

        "profile":
            profile_data,

        "profile_stats": {

            "watched_count":
                len(watched),

            "ratings_count":
                len(ratings),

            "reviews_count":
                len(reviews),

            "diary_count":
                len(diary)
        },

        "watched":
            watched,

        "ratings":
            ratings,

        "reviews":
            reviews,

        "diary":
            diary
    }


def save_profile(
    profile,
    output_path
):

    output_path = Path(
        output_path
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            profile,
            f,
            indent=4,
            ensure_ascii=False
        )