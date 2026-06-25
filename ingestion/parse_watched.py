import pandas as pd


def parse_watched(
    watched_path
):

    df = pd.read_csv(
        watched_path
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