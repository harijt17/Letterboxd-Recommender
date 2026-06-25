import pandas as pd


def parse_ratings(
    ratings_path
):

    df = pd.read_csv(
        ratings_path
    )

    if df.empty:
        return []

    df = df.where(
        pd.notnull(df),
        None
    )

    return df.to_dict(
        orient="records"
    )