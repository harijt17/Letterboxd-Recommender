from pathlib import Path


REQUIRED_FILES = [
    "profile.csv",
    "ratings.csv",
    "reviews.csv",
    "watched.csv",
    "diary.csv"
]


def validate_export(
    export_folder: Path
):

    export_folder = Path(
        export_folder
    )

    missing = []

    for file in REQUIRED_FILES:

        if not (
            export_folder / file
        ).exists():

            missing.append(file)

    return {
        "valid":
            len(missing) == 0,

        "missing_files":
            missing
    }