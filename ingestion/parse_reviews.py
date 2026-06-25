import pandas as pd


def parse_reviews(
    reviews_path
):

    df = pd.read_csv(
        reviews_path
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